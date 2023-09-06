const path = require('path');

module.exports = {
  // Im Ordner /static werden die public-Dateien abgelegt
  "outputDir": "dist",
  "devServer": {
    "contentBase": path.join(__dirname, 'public'),
    // Wird als Proxy für server.js und /app/main.js verwendet
    // Wichtig, damit CORS richtig behandelt wird
    "proxy": 'http://localhost/public',

  },
  "transpileDependencies": [
    "vuetify"
  ],
}