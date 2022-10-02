pub struct Processor {
    pub url: String,
    pub data: Option<Vec<Value>>,
    pub alert: AppAlert,
    pub db: AppDB,
}
