import httpclient
import json
import nimpy

let client = newHttpClient()

proc getAge(name, country: string): string {.exportpy.} =
  var uri = "https://api.agify.io?name="

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
  var uri: string

  if country == "":
    uri = "https://api.genderize.io?name=" & name
  else:
    uri = "https://api.genderize.io?name=" & name & "&country_id=" & country

  let
    response = parseJson(client.getContent(uri))
    gender = response["gender"].getStr()

  if gender == "":
    return "Gender unknown"

  return gender