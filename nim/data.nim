import httpclient
import json
import nimpy

let
  client = newHttpClient()

proc getAge(name, country: string): string {.exportpy.} =
  var
    uri = "https://api.agify.io?name="

  if country == "":
    uri &= name
  else:
    uri &= name & "&country_id=" & country

  let
    response = parseJson(client.getContent(uri))
    age = response["age"].getInt()

  if age < 1:
    return "Age unknown"

  return $response["age"].getInt()

proc getGender(name, country: string): string {.exportpy.} =
  var uri = "https://api.genderize.io?name="

  if country == "":
    uri &= name
  else:
    uri &= name & "&country_id=" & country

  let
    response = parseJson(client.getContent(uri))
    gender = response["gender"].getStr()

  if gender == "":
    return "Gender Unknown"

  return gender

proc getNationality(name: string): string {.exportpy.} =
  var
    country: string
    probability: float

  let
    response = parseJson(client.getContent("https://api.nationalize.io?name=" & name))
    possibleNations = response["country"].getElems()

  for i in possibleNations:
    if i["probability"].getFloat() > probability:
      probability = i["probability"].getFloat()
      country = i["country_id"].getStr()

  return country