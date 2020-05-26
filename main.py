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
from models import CurPairs
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
def api_home(request: Request, db: Session = Depends(get_db)):
	"""
	home page to display all real time values
	"""
	# try to get atleast only last 100 from db. Saves overhead; Note we use only last 26
	cur_pairs = db.query(CurPairs).order_by(CurPairs.id.desc())
	
	realtime = {
		"btcusd": cur_pairs.filter(CurPairs.cur_pair=="BTC/USD").first() ,
		"ethusd": cur_pairs.filter(CurPairs.cur_pair=="ETH/USD").first() ,
		"eurusd": cur_pairs.filter(CurPairs.cur_pair=="EUR/USD").first() ,
		"usdjpy": cur_pairs.filter(CurPairs.cur_pair=="USD/JPY").first() ,
		"gbpusd": cur_pairs.filter(CurPairs.cur_pair=="GBP/USD").first() ,
		"audusd": cur_pairs.filter(CurPairs.cur_pair=="AUD/USD").first() ,
		"nzdusd": cur_pairs.filter(CurPairs.cur_pair=="NZD/USD").first() ,
		"eurjpy": cur_pairs.filter(CurPairs.cur_pair=="EUR/JPY").first() ,
		"gbpjpy": cur_pairs.filter(CurPairs.cur_pair=="GBP/JPY").first() ,
		"eurgbp": cur_pairs.filter(CurPairs.cur_pair=="EUR/GBP").first(),
		"eurcad":	cur_pairs.filter(CurPairs.cur_pair=="EUR/CAD").first(),
		"eursek": cur_pairs.filter(CurPairs.cur_pair=="EUR/SEK").first(),
		"eurchf": cur_pairs.filter(CurPairs.cur_pair=="EUR/CHF").first(),
		"eurhuf": cur_pairs.filter(CurPairs.cur_pair=="EUR/HUF").first(),
		"eurjpy": cur_pairs.filter(CurPairs.cur_pair=="EUR/JPY").first(),
		"usdcny": cur_pairs.filter(CurPairs.cur_pair=="USD/CNY").first(),
		"usdhkd": cur_pairs.filter(CurPairs.cur_pair=="USD/HKD").first(),
		"usdsgd": cur_pairs.filter(CurPairs.cur_pair=="USD/SGD").first(),
		"usdinr": cur_pairs.filter(CurPairs.cur_pair=="USD/INR").first(),
		"usdmxn": cur_pairs.filter(CurPairs.cur_pair=="USD/MXN").first(),
		"usdphp": cur_pairs.filter(CurPairs.cur_pair=="USD/PHP").first(),
		"usdidr": cur_pairs.filter(CurPairs.cur_pair=="USDIDR").first(),
		"usdthb": cur_pairs.filter(CurPairs.cur_pair=="USD/THB").first(),
		"usdmyr": cur_pairs.filter(CurPairs.cur_pair=="USD/MYR").first(),
		"usdzar": cur_pairs.filter(CurPairs.cur_pair=="USD/ZAR").first(),
		"usdrub": cur_pairs.filter(CurPairs.cur_pair=="USD/RUB").first(),
	}
	
	context = {
		"request": request,
		"realtime": realtime
	}
	return templates.TemplateResponse("home.html", context)


@app.post("/api/currencypairs")
async def start_fetching(cur_pair_req: CurPairRequest,  background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	Starts/stops collecting realtime data and stores in db.
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