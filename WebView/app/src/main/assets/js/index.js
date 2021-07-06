var vm = new Vue({
    el: '#jddk',
    data: {
        imgs: [],
        addShow: true,
        mltoast: {
            show: false,
            text: ''
        }
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
        // 上传到后台
        submit: function () {

            var that = this;
            console.log(this.imgs);
            console.log(typeof this.imgs)

            $.ajax({
                url: 'http://10.0.2.2:5000/upload',
                dataType: 'json',
                type: 'POST',
                data: JSON.stringify(that.imgs),
                processData: false,
                contentType: false,
                success: function (res) {
                    console.log(res)
                },
                error: function () {
                    console.log('error')
                }
            })

            // axios({
            //     url: 'http://test.360guanggu.com/xyzl/weixin.php/Member/question_detail',
            //     method:'post',
            //     data: {
            //         type: 1,
            //         image: that.imgs,
            //         question:'33333',
            //         is_anonym:1
            //     },
            //     headers: {"Content-Type": "multipart/form-data"}
            // })
            // .then(function(res) {
            //     console.log(res)
            // })
            // .catch(function(error) {
            //     console.log(error);
            // });
        },
        // toast
        // toast:function(text){
        //     this.mltoast.text = text;
        //     this.mltoast.show = true;
        //     setTimeout(() => {
        //       this.mltoast.show = false;
        //     }, 1500)
        // }

    }
})