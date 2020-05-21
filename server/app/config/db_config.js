module.exports = {
    url: "mongodb://id4c.myqnapcloud.com:37011/",
    user:"qiot",
    pwd: "qiot"
  };


  /**
   ** ADMIN USER **
   * db.createUser({ user: 'team2', pwd: '118@Team2', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
   ** LOGIN COMMAND **
   * mongo -u team2 -p 118@Team2 --authenticationDatabase admin
   ** CREATE USER FROM TERMINAL **
   * db.createUser({ user: "qiot ", pwd: "qiot", roles: [ { role: "dbOwner", db: "cfiot"}]});
   */