use rocket::{get, post, put, delete, routes, State, http::Status, serde::json::Json};
use sled::Db;
use uuid::Uuid;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct Trabalho {
    id: String,
    descricao: String,
    cliente: String,
    resposta: Vec<String>,
}

impl Trabalho {
    fn new(descricao: String, cliente: String, resposta: Vec<String>) -> Trabalho {
        Trabalho {
            id: Uuid::new_v4().to_string(),
            descricao,
            cliente,
            resposta,
        }
    }
}

#[derive(Serialize, Deserialize)]
pub struct TrabalhoDTO {
    descricao: String,
    cliente: String,
    resposta: Vec<String>,
}


#[post("/trabalho", data = "<trabalho_dto>")]
fn create_trabalho(trabalho_dto: Json<TrabalhoDTO>, db: &State<Db>) -> Status {
    let trabalho = Trabalho::new(trabalho_dto.descricao.clone(), trabalho_dto.cliente.clone(), trabalho_dto.resposta.clone());
    let key = trabalho.id.as_bytes().to_vec();
    db.insert(key, serde_json::to_vec(&trabalho).unwrap()).unwrap();
    Status::Created
}


#[get("/trabalho/<id>")]
fn get_trabalho(id: &str, db: &State<Db>) -> Option<Json<Trabalho>> {
    let key = id.as_bytes().to_vec(); 
    if let Some(value) = db.get(key).unwrap(){
         let trabalho: Trabalho = serde_json::from_slice(&value).unwrap();
        Some(Json(trabalho))
    } else {
        None
    }
}


#[get("/trabalho")]
pub fn get_all_trabalhos(db: &State<Db>) -> Json<Vec<Trabalho>> {
    let mut trabalhos: Vec<Trabalho> = Vec::new();

    for item in db.iter() {
        match item {
            Ok((_key, value)) => {
                let trabalho: Trabalho = serde_json::from_slice(&value).unwrap();
                trabalhos.push(trabalho);
            },
            Err(e) => {
                println!("Erro ao iterar sobre o banco de dados: {:?}", e);
            }
        }
    }

    Json(trabalhos)
}
#[put("/trabalho/<id>", data = "<trabalho>")]
fn update_trabalho(id: &str, trabalho: Json<Trabalho>, db: &State<Db>) -> Status {
    let key = id.as_bytes().to_vec();
    db.insert(key, serde_json::to_vec(&trabalho.into_inner()).unwrap()).unwrap();
    Status::Ok
}


#[delete("/trabalho/<id>")]
fn delete_trabalho(id: &str, db: &State<Db>) -> Status {
    let key = id.as_bytes().to_vec();
    db.remove(key).unwrap();
    Status::Ok
}


#[rocket::main]
async fn main() {
    let db = sled::open("trabalho.db").unwrap();
    rocket::build()
        .manage(db)
        .mount("/", routes![create_trabalho, get_trabalho, get_all_trabalhos, update_trabalho, delete_trabalho])
        .launch()
        .await
        .unwrap();
}
