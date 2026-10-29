package de.angebote.luebeck;
import android.webkit.ValueCallback;
@SuppressWarnings({"rawtypes"})
final class BackResult implements ValueCallback {
    private final MainActivity a;
    BackResult(MainActivity a) { this.a = a; }
    @Override public void onReceiveValue(Object v) { if (!"1".equals(String.valueOf(v))) a.backFallback(); }
}
