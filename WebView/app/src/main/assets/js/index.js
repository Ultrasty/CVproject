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


        window.alert = function(msg, callback) {
            var div = document.createElement("div");
            div.innerHTML = "<style type=\"text/css\">"
                    + ".nbaMask { position: fixed; z-index: 1000; top: 0; right: 0; left: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); }                                          "
                    + ".nbaMaskTransparent { position: fixed; z-index: 1000; top: 0; right: 0; left: 0; bottom: 0; }                                               "
                    + ".nbaDialog { position: fixed; z-index: 5000; width: 80%; max-width: 300px; top: 50%; left: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); background-color: #fff; text-align: center; border-radius: 8px; overflow: hidden; opacity: 1; color: white; }"
                    + ".nbaDialog .nbaDialogHd { padding: .2rem .27rem .08rem .27rem; }                                                       "
                    + ".nbaDialog .nbaDialogHd .nbaDialogTitle { font-size: 17px; font-weight: 400; }                                                   "
                    + ".nbaDialog .nbaDialogBd { padding: 0 .27rem; font-size: 15px; line-height: 1.3; word-wrap: break-word; word-break: break-all; color: #000000; }                                   "
                    + ".nbaDialog .nbaDialogFt { position: relative; line-height: 48px; font-size: 17px; display: -webkit-box; display: -webkit-flex; display: flex; }                                   "
                    + ".nbaDialog .nbaDialogFt:after { content: \" \"; position: absolute; left: 0; top: 0; right: 0; height: 1px; border-top: 1px solid #e6e6e6; color: #e6e6e6; -webkit-transform-origin: 0 0; transform-origin: 0 0; -webkit-transform: scaleY(0.5); transform: scaleY(0.5); }    "
                    + ".nbaDialog .nbaDialogBtn { display: block; -webkit-box-flex: 1; -webkit-flex: 1; flex: 1; color: #09BB07; text-decoration: none; -webkit-tap-highlight-color: transparent; position: relative; margin-bottom: 0; }                  "
                    + ".nbaDialog .nbaDialogBtn:after { content: \" \"; position: absolute; left: 0; top: 0; width: 1px; bottom: 0; border-left: 1px solid #e6e6e6; color: #e6e6e6; -webkit-transform-origin: 0 0; transform-origin: 0 0; -webkit-transform: scaleX(0.5); transform: scaleX(0.5); }    "
                    + ".nbaDialog a { text-decoration: none; -webkit-tap-highlight-color: transparent; }"
                    + "</style>"
                    + "<div id=\"dialogs2\" style=\"display: none\">"
                    + "<div class=\"nbaMask\"></div>"
                    + "<div class=\"nbaDialog\">"
                    + " <div class=\"nbaDialogHd\">"
                    + "     <strong class=\"nbaDialogTitle\"></strong>"
                    + " </div>"
                    + " <div class=\"nbaDialogBd\" id=\"dialog_msg2\">弹窗内容，告知当前状态、信息和解决方法，描述文字尽量控制在三行内</div>"
                    + " <div class=\"nbaDialogHd\">"
                    + "     <strong class=\"nbaDialogTitle\"></strong>"
                    + " </div>"
                    + " <div class=\"nbaDialogFt\">"
                    + "     <a href=\"javascript:;\" class=\"nbaDialogBtn nbaDialogBtnPrimary\" id=\"dialog_ok2\">确定</a>"
                    + " </div></div></div>";
            document.body.appendChild(div);

            var dialogs2 = document.getElementById("dialogs2");
            dialogs2.style.display = 'block';

            var dialog_msg2 = document.getElementById("dialog_msg2");
            dialog_msg2.innerHTML = msg;

            // var dialog_cancel = document.getElementById("dialog_cancel");
            // dialog_cancel.onclick = function() {
            // dialogs2.style.display = 'none';
            // };
            var dialog_ok2 = document.getElementById("dialog_ok2");
            dialog_ok2.onclick = function() {
                dialogs2.style.display = 'none';
                callback();
            };
        };

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
                //url: 'http://10.0.2.2:5000/index',
                url: 'http://localhost:5000/index',
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
                    alert("拼接成功")
                },

                error: function () {
                    console.log('error')
                    that.loadingShow = false;
                    alert("请求失败");
                }
            })
        }
    }
})