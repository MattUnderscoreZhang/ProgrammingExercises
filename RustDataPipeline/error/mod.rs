pub enum AppErrorType {
    SerdeJsonError,
    ReqwestError,
    AwsSdkError,
    DbError,
}

#[derive(Debug, PartialEq)]
pub struct AppError {
    pub message: Option<String>,
    pub cause: Option<String>,
    pub error_type: AppErrorType,
}

impl From<serde_json:Error> for AppError {
    fn from(error: serde_json::Error) -> AppError {
        AppError {
            message: Some(error.to_string()),
            cause: Some("serde_json error".to_string()),
            error_type: AppErrorType::SerdeJsonError,
        }
    }
}
