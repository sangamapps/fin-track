const express = require('express');
const app = express();

app.set('view engine', 'ejs');

app.use(express.json());

if (process.env.IS_PROD) {
    app.use('/assets', function (req, res) {
        res.redirect("https://sangamapps.github.io/fin-track-cdn/assets/" + req.path);
    });
} else {
    app.use('/assets', express.static(__dirname + '/fin-track-ui/assets'));
}

app.get([
    '/',
    '/upload',
], function (req, res) {
    res.render("index", { userInfo: null });
});

app.all('*', (req, res) => { res.redirect("/") });

module.exports = app;