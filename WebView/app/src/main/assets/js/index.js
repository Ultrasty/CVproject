var vm = new Vue({
    el: '#jddk',
    data: {
        imgs: [],
        addShow: true,
        resultShow: false,
        loadingShow: false,
        result: [],

    },
    mounted: function () {
        this.login();
    },
    methods: {
        // 选择图片
        chooseImg: function (e) {
            var that = this;
            var files = e.target.files;
            var imgsLength = this.imgs.length;
            var maxLength = 3;
            //还可以上传的图片数量
            var count = maxLength - imgsLength;
            // 限制最多3张

            // 有选择图片

            if (files.length == 1) {
                canvasResize(files[0], {
                    crop: false,
                    quality: 0.9,
                    rotate: 0,
                    callback(baseStr) {
                        that.imgs.push(baseStr)
                    }
                })
            } else {
                for (let i = 0; i < count; i++) {
                    canvasResize(files[i], {
                        crop: false,
                        quality: 0.9,
                        rotate: 0,
                        callback(baseStr) {
                            that.imgs.push(baseStr)
                        }
                    })
                }
            }

        },
        // 删除图片
        delImg: function (index) {
            this.imgs.splice(index, 1);
            this.addShow = true;
        },
        // 登录
        login: function () {


        },

        refresh: function(){
            location.reload();
        },

        // 上传到后台
        submit: function () {

            let that = this;
            this.loadingShow = true;
            $.ajax({
                url: 'http://10.0.2.2:5000/index',
                //url: 'http://localhost:5000/index',
                //url: 'http://imsty.cn:5000/index',
                dataType: 'json',
                type: 'POST',
                // data: JSON.stringify(that.imgs),
                data: JSON.stringify({"img_l": this.imgs[0], "img_r": this.imgs[1]}),
                processData: false,
                contentType: false,
                success: function (res) {
                    console.log(res)
                    that.resultShow = true;
                    let result1 = "data:image/jpeg;base64,"+res["result1"];
                    that.result.push(result1);
                    let result2 = "data:image/jpeg;base64,"+res["result2"];
                    that.result.push(result2);
                    that.loadingShow = false;
                },

                error: function () {
                    console.log('error')
                    that.loadingShow = false;
                }
            })
        }
    }
})