// Adapted from Shopify Dawn assets/product-model.js (MIT)
(function () {
  if (!window.Shopify || !window.Shopify.loadFeatures) return;
  function setupXR(errors) {
    if (errors) return;
    if (!window.ShopifyXR) return document.addEventListener('shopify_xr_initialized', function () { setupXR(); });
    document.querySelectorAll('[id^="ProductJSON-"]').forEach(function (el) {
      window.ShopifyXR.addModels(JSON.parse(el.textContent));
      el.remove();
    });
    window.ShopifyXR.setupXRElements();
  }
  function setupUI(errors) {
    if (errors) return;
    document.querySelectorAll('.g-slide-model model-viewer').forEach(function (el) { new window.Shopify.ModelViewerUI(el); });
  }
  window.Shopify.loadFeatures([
    { name: 'shopify-xr', version: '1.0', onLoad: setupXR },
    { name: 'model-viewer-ui', version: '1.0', onLoad: setupUI }
  ]);
})();
