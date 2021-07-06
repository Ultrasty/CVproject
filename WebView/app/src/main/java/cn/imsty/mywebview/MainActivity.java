package cn.imsty.mywebview;


import android.app.Activity;
import android.os.Bundle;
import android.view.Window;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //获得控件
        WebView webView = (WebView) findViewById(R.id.wv_webview);
        //访问网页
        webView.loadUrl("http://imsty.cn");
        //系统默认会通过手机浏览器打开网页，为了能够直接通过WebView显示网页，则必须设置

        webView.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                //使用WebView加载显示url
                view.loadUrl(url);
                //返回true
                return true;
            }
        });


    }
}