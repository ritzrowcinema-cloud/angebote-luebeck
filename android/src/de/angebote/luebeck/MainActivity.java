package de.angebote.luebeck;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.FrameLayout;
import android.widget.ProgressBar;

public class MainActivity extends Activity {
    // Die Oberfläche steckt in der App; die Angebote holt sie bei jedem Start aus
    // https://raw.githubusercontent.com/ritzrowcinema-cloud/angebote-luebeck/main/data.json
    static final String START_URL = "https://" + Client.HOST + "/index.html";

    WebView web;
    ProgressBar bar;
    boolean offline = false;
    long pausedAt = 0;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(Color.parseColor("#0E1217"));
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#0E1217"));
        root.addView(web, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        bar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        bar.setIndeterminate(true);
        root.addView(bar, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 12, Gravity.TOP));
        setContentView(root);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);   // Einkaufsliste bleibt auf dem Handy gespeichert
        s.setDatabaseEnabled(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setBuiltInZoomControls(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setUserAgentString(s.getUserAgentString() + " AngeboteLuebeckApp/2.0");

        web.setWebChromeClient(new Chrome(this));
        web.setWebViewClient(new Client(this));
        if (b != null) web.restoreState(b); else web.loadUrl(START_URL);
    }

    void loadOnline() { web.loadUrl(START_URL); }
    void loadOffline() { }

    @Override protected void onSaveInstanceState(Bundle o) { super.onSaveInstanceState(o); web.saveState(o); }
    @Override protected void onPause() { super.onPause(); pausedAt = SystemClock.elapsedRealtime(); web.onPause(); }
    @Override protected void onResume() {
        super.onResume();
        web.onResume();
        // Nach 3 Stunden im Hintergrund neue Angebote holen – die Einkaufsliste bleibt dabei erhalten
        if (pausedAt > 0 && SystemClock.elapsedRealtime() - pausedAt > 3L * 60 * 60 * 1000) web.reload();
    }
    @Override public void onBackPressed() {
        web.evaluateJavascript("(function(){var s=document.getElementById('sheet'),x=document.getElementById('box');"
            + "if(x&&!x.hidden){x.hidden=true;return 1;} if(s&&!s.hidden){document.getElementById('closeList').click();return 1;} return 0;})()",
            (android.webkit.ValueCallback<String>) (android.webkit.ValueCallback) new BackResult(this));
    }
    void backFallback() { if (web.canGoBack()) web.goBack(); else finish(); }
}
