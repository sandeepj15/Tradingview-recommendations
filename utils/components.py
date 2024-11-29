#components.py
ticker_component = """
    <script type="text/javascript" src="https://files.coinmarketcap.com/static/widget/coinMarquee.js"></script><div id="coinmarketcap-widget-marquee"coins="1,1027,1839,2010,3890,5426,4195,52,74,5994,6636,5805,7083,1975,6535,3794,4030,18876,1966,6210,2011,1958,6783,7278,3513"currency="USD" theme="light" transparent="false" show-symbol-logo="true"></div>
    """
tradinfview_component = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div id="tradingview_b7851"></div>
  <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/BTCUSDT/?exchange=BINANCE" 
  rel="noopener" target="_blank"><span class="blue-text">BTCUSDT Chart</span></a> by TradingView</div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {
  "width": 750,
  "height": 540,
  "symbol" : "BINANCE:BTCUSDT",
  "interval": "D",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "in",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "withdateranges": true,
  "hide_side_toolbar": false,
  "allow_symbol_change": true,
  "container_id": "tradingview_b7851"
}
  );
  </script>
</div>
<!-- TradingView Widget END -->
"""

cryptonews_component = """
   <script src="https://www.cryptohopper.com/widgets/js/script"></script> 
   <div class="cryptohopper-web-widget" data-id="5"></div> 
    """