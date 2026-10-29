package de.angebote.luebeck;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebView;
final class Chrome extends WebChromeClient {
    private final MainActivity a;
    Chrome(MainActivity a) { this.a = a; }
    @Override public void onProgressChanged(WebView v, int p) { a.bar.setVisibility(p < 100 ? View.VISIBLE : View.GONE); }
}
