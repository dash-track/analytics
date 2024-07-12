import json
import sys, pathlib
import pickle
# Added to make consistent import paths with respect to src
sys.path.append(f"{pathlib.Path(__file__).parent.resolve()}/../..")
import constants

class curlBuilder:
    def __init__(self, base_url):
        self.base_url = base_url # can construct / get this from doordash.py
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US',
            'apollographql-client-name': '@doordash/app-consumer-production-ssr-client',
            'apollographql-client-version': '3.0',
            'content-type': 'application/json',
            'cookie': '<cookies>',
            'dnt': '1',
            'origin': 'https://www.doordash.com',
            'priority': 'u=1, i',
            'referer': 'https://www.doordash.com/orders/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-channel-id': 'marketplace',
            'x-csrftoken': '<csrftoken>',
            'x-experience-id': 'doordash'
        }
        self.data_template = {
            "operationName": "getConsumerOrdersWithDetails",
            "variables": {
                "offset": 0,
                "limit": 30,
                "includeCancelled": True
            },
            "query": """query getConsumerOrdersWithDetails($offset: Int!, $limit: Int!, $includeCancelled: Boolean) {
              getConsumerOrdersWithDetails(
                offset: $offset
                limit: $limit
                includeCancelled: $includeCancelled
              ) {
                id
                orderUuid
                deliveryUuid
                createdAt
                submittedAt
                cancelledAt
                fulfilledAt
                specialInstructions
                isConsumerSubscriptionEligible
                isGroup
                isReorderable
                isGift
                isPickup
                isMerchantShipping
                containsAlcohol
                fulfillmentType
                shoppingProtocol
                creator {
                  ...ConsumerOrderCreatorFragment
                  __typename
                }
                deliveryAddress {
                  id
                  formattedAddress
                  __typename
                }
                orders {
                  id
                  creator {
                    ...ConsumerOrderCreatorFragment
                    __typename
                  }
                  items {
                    ...ConsumerOrderOrderItemFragment
                    __typename
                  }
                  __typename
                }
                paymentCard {
                  ...ConsumerOrderPaymentCardFragment
                  __typename
                }
                grandTotal {
                  unitAmount
                  currency
                  decimalPlaces
                  displayString
                  sign
                  __typename
                }
                likelyOosItems {
                  menuItemId
                  name
                  photoUrl
                  __typename
                }
                pollingInterval
                store {
                  id
                  name
                  business {
                    id
                    name
                    __typename
                  }
                  phoneNumber
                  fulfillsOwnDeliveries
                  customerArrivedPickupInstructions
                  isPriceMatchingEnabled
                  priceMatchGuaranteeInfo {
                    headerDisplayString
                    bodyDisplayString
                    buttonDisplayString
                    __typename
                  }
                  __typename
                }
                recurringOrderDetails {
                  itemNames
                  consumerId
                  recurringOrderUpcomingOrderUuid
                  scheduledDeliveryDate
                  arrivalTimeDisplayString
                  storeName
                  isCancelled
                  __typename
                }
                bundleOrderInfo {
                  ...BundleOrderInfoFragment
                  __typename
                }
                cancellationPendingRefundInfo {
                  state
                  originalPaymentAmount {
                    unitAmount
                    currency
                    decimalPlaces
                    displayString
                    sign
                    __typename
                  }
                  creditAmount {
                    unitAmount
                    currency
                    decimalPlaces
                    displayString
                    sign
                    __typename
                  }
                  __typename
                }
                __typename
              }
            }
            
            fragment ConsumerOrderPaymentCardFragment on ConsumerOrderPaymentCard {
              id
              last4
              type
              __typename
            }
            
            fragment ConsumerOrderOrderItemFragment on ConsumerOrderOrderItem {
              id
              name
              quantity
              specialInstructions
              substitutionPreferences
              orderItemExtras {
                ...ConsumerOrderOrderItemExtraFragment
                __typename
              }
              purchaseQuantity {
                ...ConsumerOrderQuantityFragment
                __typename
              }
              fulfillQuantity {
                ...ConsumerOrderQuantityFragment
                __typename
              }
              originalItemPrice
              purchaseType
              __typename
            }
            
            fragment ConsumerOrderOrderItemExtraOptionFields on OrderItemExtraOption {
              menuExtraOptionId
              name
              description
              price
              quantity
              __typename
            }
            
            fragment ConsumerOrderOrderItemExtraOptionFragment on OrderItemExtraOption {
              ...ConsumerOrderOrderItemExtraOptionFields
              orderItemExtras {
                ...ConsumerOrderOrderItemExtraFields
                orderItemExtraOptions {
                  ...ConsumerOrderOrderItemExtraOptionFields
                  orderItemExtras {
                    ...ConsumerOrderOrderItemExtraFields
                    __typename
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            
            fragment ConsumerOrderOrderItemExtraFields on OrderItemExtra {
              menuItemExtraId
              name
              __typename
            }
            
            fragment ConsumerOrderOrderItemExtraFragment on OrderItemExtra {
              ...ConsumerOrderOrderItemExtraFields
              orderItemExtraOptions {
                ...ConsumerOrderOrderItemExtraOptionFragment
                __typename
              }
              __typename
            }
            
            fragment ConsumerOrderCreatorFragment on ConsumerOrderCreator {
              id
              firstName
              lastName
              __typename
            }
            
            fragment ConsumerOrderQuantityFragment on Quantity {
              continuousQuantity {
                quantity
                unit
                __typename
              }
              discreteQuantity {
                quantity
                unit
                __typename
              }
              __typename
            }
            
            fragment BundleOrderInfoFragment on BundleOrderInfo {
              primaryBundleOrderUuid
              primaryBundleOrderId
              bundleOrderUuids
              bundleOrderConfig {
                ...BundleOrderConfigFragment
                __typename
              }
              __typename
            }
            
            fragment BundleOrderConfigFragment on BundleOrderConfig {
              bundleType
              bundleOrderRole
              __typename
            }"""
        }

    def get_cookies(self):
        try:
            with open(constants.CHROME_DRIVER_COOKIE_DIR, "rb") as file:
                cookies = pickle.load(file)
        except Exception as e:
            print("Error loading cookies from file: ", e)
            return
        
        cookie_list = []
        for cookie in cookies:
            cookie_list.append(f"{cookie['name']}={cookie['value']}")
            if cookie['name'] == 'csrf_token':
                self.headers['x-csrftoken'] = cookie['value']
        
        cookie_str = '; '.join(cookie_list)
        self.headers['cookie'] = cookie_str

    
    def build_curl_command(self, offset=0, limit=30, include_cancelled=True):
        self.data_template['variables']['offset'] = offset
        self.data_template['variables']['limit'] = limit
        self.data_template['variables']['includeCancelled'] = include_cancelled

        headers = ' '.join([f"-H '{k}: {v}'" for k, v in self.headers.items()])
        data = json.dumps(self.data_template)
        curl_command = f"curl '{self.base_url}' {headers} --data-raw '{data}'"
        return curl_command

"""
Main for dev testing
"""
class Main():
    def __init__(self):
        self.cb = curlBuilder("https://www.doordash.com/")
        self.cb.get_cookies()
        print(self.cb.build_curl_command(0, 30, True))

if __name__ == "__main__":
    Main()