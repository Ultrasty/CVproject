import numpy as np
import cv2


def drawMatches(imageA, imageB, keyPointsA, keyPointsB, matches, status):
    (hA, wA) = imageA.shape[:2]
    (hB, wB) = imageB.shape[:2]
    vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
    vis[0:hA, 0:wA] = imageA
    vis[0:hB, wA:] = imageB

    for ((trainIdx, queryIdx), s) in zip(matches, status):
        # only process the match if the keypoint was successfully
        if s == 1:
            # draw the match
            pointA = (int(keyPointsA[queryIdx][0]), int(keyPointsA[queryIdx][1]))
            pointB = (int(keyPointsB[trainIdx][0]) + wA, int(keyPointsB[trainIdx][1]))
            cv2.line(vis, pointA, pointB, (0, 0, 255), 1)
    return vis


def matchKeyPoints(keyPointsA, keyPointsB, featuresA, featuresB, ratio, reprojThresh):
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
    matches = []

    # loop over the raw matches
    for m in rawMatches:
        # ensure the distance is within a certain ratio of each
        # other (i.e. Lowe's ratio test)
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            matches.append((m[0].trainIdx, m[0].queryIdx))

    # RANSAC Algorithm
    # computing homography matrix needs at least four matching points
    if len(matches) > 4:
        # construct the two sets of points
        pointsA = np.float32([keyPointsA[i] for (_, i) in matches])
        pointsB = np.float32([keyPointsB[i] for (i, _) in matches])

        # compute the homography between the two sets of points
        (H, status) = cv2.findHomography(pointsA, pointsB, cv2.RANSAC, reprojThresh)

        # return the matches along with the homography matrix and status of each matched point
        return matches, H, status

    return None


# 接收照片，检测关键点和提取局部不变特征
# 用到了高斯差分（Difference of Gaussian (DoG)）关键点检测，和SIFT特征提取
# detectAndCompute方法用来处理提取关键点和特征
# 返回一系列的关键点
def detectAndDescribe(image):
    # detect and extract features from the image
    descriptor = cv2.xfeatures2d.SIFT_create()
    (keyPoints, features) = descriptor.detectAndCompute(image, None)
    keyPoints = np.float32([kp.point for kp in keyPoints])
    # return a tuple of keyPoints and features
    return keyPoints, features


def stitch(images, ratio=0.75, reprojThresh=4.0,
           showMatches=False):
    # unpack the images, then detect keyPoints and extract
    # local invariant descriptors from them

    (imageB, imageA) = images
    (keyPointsA, featuresA) = detectAndDescribe(imageA)
    (keyPointsB, featuresB) = detectAndDescribe(imageB)

    # match features between the two images

    (matches, H, status) = matchKeyPoints(keyPointsA, keyPointsB, featuresA, featuresB, ratio, reprojThresh)
    # if the match is None, then there aren't enough matched
    # keyPoints to create a panorama

    result = cv2.warpPerspective(imageA, H, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
    result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

    # check to see if the keypoint matches should be visualized
    if showMatches:
        vis = drawMatches(imageA, imageB, keyPointsA, keyPointsB, matches, status)
        # return a tuple of the stitched image and the
        # visualization
        return result, vis

    # return the stitched image
    return result


def colorCorrection(images_temp, shift, bestIndex, gamma=2.2):  # set gamma to 2.2 by paper
    alpha = np.ones((3, len(images_temp)))

    # compute light averages in the overlap area by linearizing the gamma-corrected RGB values
    for rightBorder in range(bestIndex + 1, len(images_temp)):
        for i in range(bestIndex + 1, rightBorder + 1):
            I = images_temp[i]
            J = images_temp[i - 1]
            overlap = I.shape[1] - shift[i - 1]
            for channel in range(3):
                alpha[channel, i] = np.sum(np.power(J[:, -overlap - 1:, channel], gamma)) / np.sum(
                    np.power(I[:, 0:overlap + 1, channel], gamma))  # derivative

        G = np.sum(alpha, 1) / np.sum(np.square(alpha), 1)

        for i in range(bestIndex + 1, rightBorder + 1):
            for channel in range(3):
                images_temp[i][:, :, channel] = np.power(G[channel] * alpha[channel, i], 1.0 / gamma) * images_temp[i][
                                                                                                        :, :,
                                                                                                        channel]  # perform using correction coefficients and the global adjustment

    for leftBorder in range(bestIndex - 1, -1, -1):
        for i in range(bestIndex - 1, leftBorder - 1, -1):
            I = images_temp[i]
            J = images_temp[i + 1]
            overlap = I.shape[1] - shift[i - 1]
            for channel in range(3):
                alpha[channel, i] = np.sum(np.power(J[:, 0:overlap + 1, channel], gamma)) / np.sum(
                    np.power(I[:, -overlap - 1:, channel], gamma))

        G = np.sum(alpha, 1) / np.sum(np.square(alpha), 1)

        for i in range(bestIndex - 1, leftBorder - 1, -1):
            for channel in range(3):
                images_temp[i][:, :, channel] = np.power(G[channel] * alpha[channel, i], 1.0 / gamma) * images_temp[i][
                                                                                                        :, :, channel]
    return images_temp


if __name__ == '__main__':
    ImageA = cv2.imread('test1.jpg')
    ImageB = cv2.imread('test2.jpg')
    (Result, Vis) = stitch([ImageA, ImageB], showMatches=True)

    cv2.imwrite('vis1.jpg', Vis)
    cv2.imwrite('result.jpg', Result)
