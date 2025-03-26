function getStageConfigs() {
    if (process.env.IS_PROD) {
        return {
            MONGO_DB_URL: "",
            MONGO_DB_NAME: "fin-track",
            JWT_SECRET_KEY: "",
        };
    }
    return {
        MONGO_DB_URL: "",
        MONGO_DB_NAME: "fin-track-beta",
        JWT_SECRET_KEY: "",
    };
}
module.exports = Object.assign({
    PORT: process.env.PORT || 8080,
}, getStageConfigs());