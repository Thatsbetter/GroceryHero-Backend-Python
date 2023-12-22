
def register_user(self, age, email, location, name, password):
    if (not checkUserExists(email)):
        # Generate new Password Hash
        hash = generatePasswordHash(password).hex()

        new_user = RegisteredUser(name=name, age=age, email=email, password=hash, location=location)
        session.add(new_user)
        session.commit()

        status = 201
    else:
        status = 409
    return status

def login_user(self, email, password):
    result = session.query(RegisteredUser).filter(RegisteredUser.email == email).all()
    session.close()
    if (len(result) == 1):
        user = result[0]
        hash = user.password

        if (checkPasswordHash(password, hash)):
            status = 200
        else:
            status = 401
    else:
        status = 404
    return status
def delete_user(name,email):

    if checkUserExists(email):
        # checks if name and email are the same
        address = session.query(RegisteredUser).filter(
            and_(RegisteredUser.email == email,
                 RegisteredUser.name == name))
        address.delete()
        session.commit()
        session.close()