import httplib, urllib, base64, argparse, json

def init_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--api_key",
    type=str,
    default="",
    help="WMATA API key")
  parser.add_argument(
    "--origin_station_code",
    type=str,
    default="",
    help="WMATA station code where you will be starting")
  parser.add_argument(
    "--direction_of_travel",
    type=str,
    default="",
    help="Train's direction of travel (end-of-line WMATA station code)")
  parser.add_argument(
    "--walk_delay",
    type=int,
    default=0,
    help="Number of minutes to delay prediction for walk")
  return parser

def call_api():
  headers = {
    'api_key': FLAGS.api_key,
  }
  try:
    conn = httplib.HTTPSConnection('api.wmata.com')
    station = FLAGS.origin_station_code
    path = "/StationPrediction.svc/json/GetPrediction/%s" % station
    conn.request("GET", path, "", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return json.loads(data)
  except Exception as e:
    print(e)

def get_next_train_time(train_data):
  for train in train_data["Trains"]:
    if train["DestinationCode"] == FLAGS.direction_of_travel and train["Min"] != "BRD" and train["Min"] != "ARR" and train["Min"] != "---," and train["Min"] != "":
      time = int(train["Min"]) - FLAGS.walk_delay
      if time > 0:
        return time
  return -1

parser = init_parser()
FLAGS, unparsed = parser.parse_known_args()

train_data = call_api()
time = get_next_train_time(train_data)
print("You will be waiting about %d minutes on the platform." % time)