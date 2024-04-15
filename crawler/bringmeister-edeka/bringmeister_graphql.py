import time

import requests
import json
from fp.fp import FreeProxy

url = "https://www.bringmeister.de/graphql"
proxies = {
    'http': FreeProxy(elite=True).get(),
}
print(proxies)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Content-Type": "application/json",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1"
}

variables = {
    "sorting": "DEFAULT",
    "query": "",
    "zipcode": "13355",
    "pageSize": 500,
    "cursor": None  # Initialize cursor to None for the first request
}
has_next_page = True
counter = 0

while has_next_page:
    # Set the cursor for the current request
    payload = {
        "query": """
            query Search(
              $query: String!,
              $pageSize: Int!,
              $zipcode: String!,
              $sorting: ProductSorting!,
              $categoryLvl0: String,
              $categoryLvl1: String,
              $categoryLvl2: String,
              $categoryLvl3: String,
              $brand: String,
              $characteristic: [String!],
              $isAvailable: Boolean,
              $campaign: String,
              $cursor: String
            ) {
              products(
                query: $query
                first: $pageSize
                zipcode: $zipcode
                sorting: $sorting
                filter: {
                  hierarchicalCategoriesLvl0: $categoryLvl0,
                  hierarchicalCategoriesLvl1: $categoryLvl1,
                  hierarchicalCategoriesLvl2: $categoryLvl2,
                  hierarchicalCategoriesLvl3: $categoryLvl3,
                  brand: $brand,
                  characteristic: $characteristic,
                  isAvailable: $isAvailable
                }
                campaign: $campaign
                after: $cursor
              ) {
                pageInfo {
                  totalCount
                  startCursor
                  endCursor
                  hasNextPage
                  facets {
                    ...FacetsWithCategoriesFields
                  }
                  searchProviderInfos {
                    __typename
                  }
                }
                edges {
                  ...ProductsEdgeFields
                }
              }
              searchAd(query: $query, zipCode: $zipcode) {
                ...SearchAdFields
              }
            }

            fragment FacetsWithCategoriesFields on Facets {
              ...BasicFacetsFields
              ...CategoryFacetFields
            }

            fragment BasicFacetsFields on Facets {
              brand {
                name
                total
              }
              characteristic {
                name
                total
              }
            }

            fragment CategoryFacetFields on Facets {
              hierarchicalCategoriesLvl0 {
                name
                total
              }
              hierarchicalCategoriesLvl1 {
                name
                total
              }
              hierarchicalCategoriesLvl2 {
                name
                total
              }
              hierarchicalCategoriesLvl3 {
                name
                total
              }
            }

            fragment ProductsEdgeFields on ProductsEdge {
              cursor
              node {
                ...ProductNodeFields
              }
            }

            fragment ProductNodeFields on Product {
              id
              productId
              name
              isAvailable
              isBasePrice
              packing
              packingShort
              packagingMaterial
              units {
                ...ProductUnitFields
              }
              sku
              image
              properties
              browserUrl
              prices {
                price
                specialDiscount
                specialPrice
                specialBasePrice
                specialStartDateTs
                specialEndDateTs
                basePrice
                baseUnit
                deposit
              }
              depositType
              rootCategory {
                id
                name
                path
                position
              }
              hierarchicalCategories {
                name
              }
              multibuy {
                label
                type
                startTs
                endTs
              }
              bubble {
                unit
                amount
              }
              ageRestricted
              multipacks {
                sku
                isAvailable
                prices {
                  specialDiscount
                  specialPrice
                  specialStartDateTs
                  specialEndDateTs
                  basePrice
                  baseUnit
                  deposit
                }
                packing
                packingShort
                state
              }
            }

            fragment ProductUnitFields on ProductUnit {
              id
              unitId
              name
              default
              price
              specialPrice
              strikeThroughPrice
            }

            fragment SearchAdFields on SearchAd {
              __typename
              ... on SearchAdAdvertiseTile {
                ...SearchAdAdvertiseTileFields
              }
              ... on SearchAdAdvertiseRow {
                ...SearchAdAdvertiseRowFields
              }
            }

            fragment SearchAdAdvertiseTileFields on SearchAdAdvertiseTile {
              id
              text
              textColor
              textShadowColor
              backgroundColor
              image {
                ...ImageFields
              }
              imageMobile {
                ...ImageFields
              }
              link
              ageVerificationNeeded
            }

            fragment ImageFields on ContentImage {
              title
              description
              url
              width
              height
            }

            fragment SearchAdAdvertiseRowFields on SearchAdAdvertiseRow {
              id
              text
              textColor
              textShadowColor
              buttonText
              buttonTextColor
              buttonBackgroundColor
              backgroundColor
              backgroundImage {
                ...ImageFields
              }
              link
              products(first: 6) {
                edges {
                  node {
                    ...ProductForWidgetFields
                  }
                }
                pageInfo {
                  totalCount
                }
              }
              ageVerificationNeeded
            }

            fragment ProductForWidgetFields on Product {
              id
              productId
              hierarchicalCategories {
                name
                url
              }
              browserUrl
              isBasePrice
              sku
              prices {
                basePrice
                baseUnit
                deposit
                specialDiscount
                specialBasePrice
                specialPrice
                specialStartDateTs
                specialEndDateTs
                price
              }
              isAvailable
              depositType
              units {
                id
                unitId
                name
                default
                price
                specialPrice
                strikeThroughPrice
              }
              name
              packing
              packingShort
              packagingMaterial
              image
              properties
              multibuy {
                label
                type
                startTs
                endTs
              }
              bubble {
                unit
                amount
              }
              multipacks {
                sku
                isAvailable
                prices {
                  specialDiscount
                  specialPrice
                  specialStartDateTs
                  specialEndDateTs
                  basePrice
                  baseUnit
                  deposit
                }
                packingShort
                packing
                state
              }
            }
        """,
        "variables":variables
    }

    # Make the request
    response = requests.post(url, json=payload, headers=headers,proxies=proxies)

    # Update the cursor for the next request
    data = response.json().get("data", {})
    print(len(data["products"]["edges"]))
    with open(f"backup_while_graphql_response{counter}.txt", "w", encoding="utf-8") as file:
        file.write(response.text)

    pageInfo = data.get("products", {}).get("pageInfo", {})
    has_next_page = pageInfo.get("hasNextPage", False)
    print(pageInfo.get("hasNextPage", False))
    variables["cursor"] = data["products"]["edges"][-1]["cursor"] or None
    with open(f"while_graphql_response{counter}.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    counter= counter+1
    time.sleep(2)

