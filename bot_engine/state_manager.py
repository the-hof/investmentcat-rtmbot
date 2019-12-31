from tinydb import TinyDB, Query

state_db = TinyDB('state_db.json')

def get_user_state(user):
    try:
        UserState = Query()
        result = state_db.search(UserState.slack_user == user)
        if len(result) > 0:
            return result[0].get("state", {})
        return {}
    except Exception as e:
        print ("ERROR GETTING STATE")
        print (str(e))
        return {}

def save_user_state(user, state):
    try:
        UserState = Query()
        state_db.upsert({'slack_user': user, 'state': state}, UserState.slack_user == user)
    except Exception as e:
        print("ERROR SAVING STATE for user {user} : {state} ")
        print(str(e))
