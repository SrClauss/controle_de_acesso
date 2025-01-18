#[macro_use] extern crate rocket;

use serde::{Serialize, Deserialize};
use rocket::serde::json::Json;
use rocket::State;
use uuid::Uuid;
use sled::Db;
use rocket::http::Status;

#[derive(Serialize, Deserialize, Debug)]
pub struct Trabalho {
    id: String,
    descricao: String,
    cliente: String,
    resposta: Vec<String>
}




impl Trabalho {
    pub fn new(descricao: String, cliente: String, resposta: Vec<String>) -> Self {
        Trabalho {
            id: Uuid::new_v4().to_string(),
            descricao,
            cliente,
            resposta

        }
    }
}
#[derive(Serialize, Deserialize)]

pub struct TrabalhoDTO{
    pub descricao: String,
    pub cliente: String,
    pub resposta: Vec<String>
}


#[get("/trabalho")]
fn get_trabalhos(db: &State<Db>) -> Json<Vec<Trabalho>> {
    let trabalhos = db.into_iter().map(|r| r.unwrap()).map(|(_, v)| {
        serde_json::from_slice::<Trabalho>(&v).unwrap()
    }).collect::<Vec<_>>();
    Json(trabalhos)

   
}
#[get("/trabalho/<id>")]
fn get_trabalho(id: &str, db: &State<Db>) -> Option<Json<Trabalho>> {
    println!("Procurando trabalho com ID: {}", id);
    let trabalho = db.get(id).unwrap().map(|v| {
        serde_json::from_slice::<Trabalho>(&v).unwrap()
    });
    println!("Trabalho encontrado: {:?}", trabalho);
    trabalho.map(Json)
}
#[post("/trabalho", data = "<trabalho>")]
fn create_trabalho(trabalho: Json<TrabalhoDTO>, db: &State<Db>) -> Status {
    let trabalho = Trabalho::new(trabalho.descricao.clone(), trabalho.cliente.clone(), trabalho.resposta.clone());
    db.insert(trabalho.id.clone(), serde_json::to_vec(&trabalho).unwrap()).unwrap();
    Status::Created
}

#[delete("/trabalho/<id>")]
fn delete_trabalho(id: &str, db: &State<Db>) -> Status {
    db.remove(id).unwrap();
    Status::NoContent
}
#[put("/trabalho/<id>", data = "<trabalho>")]
fn update_trabalho(id: &str, trabalho: Json<TrabalhoDTO>, db: &State<Db>) -> Status {
    let trabalho = Trabalho::new(trabalho.descricao.clone(), trabalho.cliente.clone(), trabalho.resposta.clone());
    db.insert(id, serde_json::to_vec(&trabalho).unwrap()).unwrap();
    Status::Ok
}

#[launch]
fn rocket() -> _ {
    let db = sled::open("trabalhos.db").unwrap();
    rocket::build()
        .mount("/", routes![get_trabalhos, get_trabalho, create_trabalho, delete_trabalho, update_trabalho])
        .manage(db)
}