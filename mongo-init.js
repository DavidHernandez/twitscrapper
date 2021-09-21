db.createUser(
  {
    user: "twitscrapper",  // CHANGE USER
    pwd: "twitscrapper",  // CHANGE PASSWORD
    roles: [
      {
        role: "readWrite",
        db: "twitscrapper"  // CHANGE DB_NAME
      }
    ]
  }
);
