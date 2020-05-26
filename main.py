# ----------------------------------------
# create fastapi app 
# ----------------------------------------
from fastapi import FastAPI
app = FastAPI()


# ----------------------------------------
# setup templates folder
# ----------------------------------------
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


# ----------------------------------------
# setup db
# ----------------------------------------
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine) #creates tables
# stocks db will appear once you run uvicorn.
# get into sqlite and try `.schema`


# ----------------------------------------
# import custom modules
# ----------------------------------------
from scraper import CurPairScraper


# ----------------------------------------
# dependency injection
# ----------------------------------------
from fastapi import Depends

def get_db():
	""" returns db session """
	
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close


# ----------------------------------------
# bg tasks
# ----------------------------------------
from fastapi import BackgroundTasks

collect = True
def fetch_real_time():
	
	db = SessionLocal()
	
	global collect
	while (collect):
		
		all_pairs_scraper = CurPairScraper("https://finance.yahoo.com/currencies")
		
		for pair_info in all_pairs_scraper.obj_genrator():
			print("{} of {} : {}".format(pair_info["row_num"], pair_info["total_rows"], pair_info["name"]))
			curPair            = models.CurPairs()
			curPair.cur_pair   = pair_info["name"]
			curPair.price      = pair_info["price"]
			curPair.change     = pair_info["change"]
			curPair.per_change = pair_info["per_change"]
			db.add(curPair)
		db.commit()


# ----------------------------------------
# define structure for requests (Pydantic & more)
# ----------------------------------------
from fastapi import Request # for get
from pydantic import BaseModel # for post
	
class CurPairRequest(BaseModel):
	status: str


# ----------------------------------------
# ----------------------------------------
# routes and related funcs
# ----------------------------------------
# ----------------------------------------
@app.get("/")
def api_home(request: Request):
	"""
	home page to display all real time values
	"""
	
	context = {
		"request": request
	}
	return templates.TemplateResponse("home.html", context)


@app.post("/api/curencypairs")
async def start_fetching(cur_pair_req: CurPairRequest,  background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	adds given currecy pair TABLEs to db
	"""
	global collect
	if cur_pair_req.status == "STOP":
		collect = False
	if cur_pair_req.status == "START":
		collect = True
		background_tasks.add_task(fetch_real_time)
	
	"""
	curPair = models.CurPairs()
	curPair.cur_pair = cur_pair_req.cur_pair
	db.add(curPair)
	db.commit()
		
	# in correct place
	background_tasks.add_task(fetch_real_time, curPair.id)
	"""
	
	return {"status": "ok"}



# ----------------------------------------
# end
# ----------------------------------------