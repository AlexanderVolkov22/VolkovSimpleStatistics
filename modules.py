import aiosqlite


async def getinfo(token):
    db = await aiosqlite.connect('stats.sqlite')
    c = await db.execute("SELECT botname FROM tokens WHERE apitoken LIKE ?", [token])
    resp = await c.fetchone()
    await db.close()
    if resp == []:
        resp = "Wrong Token!"
        return resp
    else:
        resp = str(resp)
        resp = resp.replace("('", "")
        resp = resp.replace("',)", "")
        return resp


async def chktoken(token):
    db = await aiosqlite.connect('stats.sqlite')
    c = await db.execute("SELECT botname FROM tokens WHERE apitoken LIKE ?", [token])
    resp = await c.fetchall()
    await db.close()
    if resp == []:
        resp = "Wrong Token!"
        return resp
    else:
        resp = "True"
        return resp


async def resp_register(text, token):
    db = await aiosqlite.connect('stats.sqlite')
    c = await db.execute("SELECT text FROM stats WHERE text LIKE ? and token like ?", [text, token])
    resp = await c.fetchall()
    if resp == []:
        req = 1
        await db.execute("INSERT INTO stats VALUES(?,?,?)", [text, req, token])
        await db.commit()
        await db.close()
    else:
        c = await db.execute("SELECT requests FROM stats WHERE text LIKE ? and token like ?", [text, token])
        request_duty = str(await c.fetchone())
        request = request_duty.replace("(", "")
        request = int(request.replace(",)", ""))
        request = request + 1
        await db.execute("UPDATE stats SET requests = ? WHERE text LIKE ? and token like ?", [request, text, token])
        await db.commit()
        await db.close()


