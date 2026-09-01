# Terminal Output Notes

This file captures the key terminal and API outputs collected from the screenshots in the `images/` folder.

## 1) Product creation with automatic Gemini classification

Source image: `images/image.png`

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"title":"Perfume Glass Bottle","description":"Fragile glass container for liquid","length":6,"width":6,"height":14,"weight":0.35}'

id          : 14
title       : Perfume Glass Bottle
description : Fragile glass container for liquid
length      : 6.0
width       : 6.0
height      : 14.0
weight      : 0.35
category    : FRAGILE
```

This shows that the product endpoint accepted the payload and assigned the `FRAGILE` category.

## 2) Product creation formatted with PowerShell output

Source image: `images/image.png`

```powershell
PS C:\Users\suhri> $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"title":"Perfume Glass Bottle","description":"Fragile glass container for liquid","length":6,"width":6,"height":14,"weight":0.35}'
PS C:\Users\suhri> $response | Format-List

id          : 15
title       : Perfume Glass Bottle
description : Fragile glass container for liquid
length      : 6.0
width       : 6.0
height      : 14.0
weight      : 0.35
category    : FRAGILE
```

This demonstrates the same product creation flow when the response is assigned to a variable and displayed with `Format-List`.

## 3) Recommendation result for a liquid + fragile mixed order

Source image: `images/Screenshot 2026-09-01 220219.png`

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommend-box/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"items":[{"title":"Perfume Glass Bottle","length":6,"width":6,"height":14,"weight":0.35,"category":"LIQUID","quantity":2},{"title":"Compact Makeup Mirror","length":10,"width":10,"height":2,"weight":0.25,"category":"FRAGILE","quantity":1}]}'
```

The raw result in this case is a `No compatible box found for the given items` error when the category/size rules do not match a single box record.

This confirmed the rule that the recommendation engine requires one valid box that matches the combined category set and dimension constraints.

## 4) Successful recommendation for a single APPAREL item

Source image: `images/Screenshot 2026-09-01 220400.png`

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommend-box/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"items":[{"title":"Denim Jeans","length":14,"width":12,"height":3,"weight":0.8,"category":"APPAREL","quantity":1}]}'

box_id              : 1
box_name            : Standard Small
length              : 20.0
width               : 15.0
height              : 10.0
max_weight          : 5.0
cost                : 15.0
allowed_categories  : {STANDARD, APPAREL}
total_weight        : 0.8
required_dimensions : @{length=14.0; width=12.0; height=3.0}
```

This is the expected success path for a lightweight apparel item when the box supports `APPAREL` and fits the dimensions.

## 5) Box creation examples

Source image: `images/Screenshot 2026-09-01 220648.png`

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/boxes/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"name":"Fragile Box","length":25,"width":20,"height":18,"max_weight":6,"cost":"28.00","allowed_categories":["FRAGILE","STANDARD"]}'

id                 : 8
name               : Fragile Box
length             : 25.0
width              : 20.0
height             : 18.0
max_weight         : 6.0
cost               : 28.00
allowed_categories : {FRAGILE, STANDARD}
volume             : 9000.0
```

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/boxes/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"name":"Liquid Box","length":28,"width":18,"height":20,"max_weight":7,"cost":"25.00","allowed_categories":["LIQUID","STANDARD"]}'

id                 : 9
name               : Liquid Box
length             : 28.0
width              : 18.0
height             : 20.0
max_weight         : 7.0
cost               : 25.00
allowed_categories : {LIQUID, STANDARD}
volume             : 10080.0
```

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/boxes/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"name":"Heavy Duty Box","length":35,"width":30,"height":30,"max_weight":30,"cost":"50.00","allowed_categories":["HEAVY_DUTY","STANDARD"]}'

id                 : 10
name               : Heavy Duty Box
length             : 35.0
width              : 30.0
height             : 30.0
max_weight         : 30.0
cost               : 50.00
allowed_categories : {HEAVY_DUTY, STANDARD}
volume             : 31500.0
```

These examples show the box catalog being populated with category-based box definitions.

## 6) Mixed goods recommendation output

Source image: `images/Screenshot 2026-09-01 220219.png`

```powershell
PS C:\Users\suhri> Invoke-RestMethod -Uri "http://localhost:8000/api/v1/recommend-box/" `
>>   -Method Post `
>>   -ContentType "application/json" `
>>   -Body '{"items":[{"title":"Perfume Glass Bottle","length":6,"width":6,"height":14,"weight":0.35,"category":"LIQUID","quantity":2},{"title":"Compact Makeup Mirror","length":10,"width":10,"height":2,"weight":0.25,"category":"FRAGILE","quantity":1}]}'

box_id              : 11
box_name            : Mixed Goods Box
length              : 40.0
width               : 30.0
height             : 30.0
max_weight          : 20.0
cost                : 60.0
allowed_categories  : {APPAREL, HEAVY_DUTY, FRAGILE, LIQUID, ...}
total_weight        : 0.95
required_dimensions : @{length=12.0; width=12.0; height=28.0}
```

This confirms the recommendation engine works when a box supports the combined category set and the combined dimensions remain within the box constraints.

## 7) Django startup and Gemini fallback log

Source image: `images/Screenshot 2026-09-01 220400.png`

```text
WARNING: This is a development server. Do not use it in a production setting.
...
Starting development server at http://127.0.0.1:8000/
Performing system checks...
System check identified no issues (0 silenced).
Django version 6.1, using settings box_picker_project.settings

Gemini category classification failed; fallback to STANDARD
Traceback (most recent call last):
...
```

This log demonstrates the safety fallback behavior when the Gemini API call fails or the API key is unavailable. In that case, the system still stays alive and returns a safe `STANDARD` category instead of crashing the request.

## Summary

These terminal outputs show that:

- product creation works through the API
- Gemini classification can assign a category automatically
- box creation works for category-specific box types
- the recommendation engine selects the cheapest compatible box when the rules match
- fallback behavior is active when Gemini fails
