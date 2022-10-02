use async_trait::async_trait;
use core::fmt::Debug;

use crate::app_error::AppError;
pub mod slack;

#[async_trait(?Send)]
pub trait Producer {
    async fn run(&self, msg: &str) -> Result<(), AppError>;
}

impl Debug for dyn Producer {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        write!(f, "Producer{{{:?}}}", self)
    }
}

#[derive(Debug)]
pub struct AppAlert {
    producer: Box<dyn Producer>,
}

impl AppAlert {
    pub async fn producer(&self, msg: &str) -> Result<(), AppError> {
        self.producer.run(msg).await
    }

    pub fn new(producer: Box<dyn Producer>) -> Self {
        AppAlert { producer }
    }
}
