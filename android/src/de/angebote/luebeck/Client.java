package de.angebote.luebeck;
import android.content.Intent;
import android.net.Uri;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.InputStream;
final class Client extends WebViewClient {
    // Reservierte Adresse für App-eigene Dateien (wie WebViewAssetLoader)
    static final String HOST = "appassets.androidplatform.net";
    private final MainActivity a;
    Client(MainActivity a) { this.a = a; }
    @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
        Uri u = r.getUrl();
        if (HOST.equals(u.getHost())) {
            String path = u.getPath() == null || u.getPath().equals("/") ? "index.html" : u.getPath().substring(1);
            if (path.contains("..")) return null;
            try {
                InputStream in = a.getAssets().open(path);
                String mime = path.endsWith(".html") ? "text/html" : path.endsWith(".js") ? "application/javascript" : path.endsWith(".png") ? "image/png" : "application/octet-stream";
                return new WebResourceResponse(mime, "utf-8", in);
            } catch (Exception e) { return null; }
        }
        return null;
    }
    @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
        Uri u = r.getUrl();
        if (HOST.equals(u.getHost())) return false;
        try { a.startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception e) { }
        return true;
    }
}
