from server_client_databse_1.db_service import YmaticsDBService as _ydb

ydb = _ydb()

ydb.read()


#ydb.delete(7)
#ydb.close()
#ydb.update(1, "Derek Jeter", 25)
# ydb.create("aaa", 1)
# ydb.create("bbb", 2)
# ydb.create("ccc", 3)

# ydb.delete(7)
# ydb.delete(8)

# ydb.truncate_table()

# ydb.create("Derek Jeter", 25)
# ydb.create("Robinson Cano", 22)
# ydb.create("Alex Rodriguez", 24)
# ydb.create("Mariano Rivera", 27)
# ydb.create("Jorge Posada", 26)
# ydb.create("Carl Crawford", 22)
# ydb.create("BJ Upton", 19)

ydb.read()
ydb.close()