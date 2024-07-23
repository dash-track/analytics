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
            'accept-language': 'en-GB',
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
        self.data_template = {"operationName":"getConsumerOrdersWithDetails","variables":{"offset":0,"limit":30,"includeCancelled":True},"query":"query getConsumerOrdersWithDetails($offset: Int\u0021, $limit: Int\u0021, $includeCancelled: Boolean) {\\n  getConsumerOrdersWithDetails(\\n    offset: $offset\\n    limit: $limit\\n    includeCancelled: $includeCancelled\\n  ) {\\n    id\\n    orderUuid\\n    deliveryUuid\\n    createdAt\\n    submittedAt\\n    cancelledAt\\n    fulfilledAt\\n    specialInstructions\\n    isConsumerSubscriptionEligible\\n    isGroup\\n    isReorderable\\n    isGift\\n    isPickup\\n    isMerchantShipping\\n    containsAlcohol\\n    fulfillmentType\\n    shoppingProtocol\\n    creator {\\n      ...ConsumerOrderCreatorFragment\\n      __typename\\n    }\\n    deliveryAddress {\\n      id\\n      formattedAddress\\n      __typename\\n    }\\n    orders {\\n      id\\n      creator {\\n        ...ConsumerOrderCreatorFragment\\n        __typename\\n      }\\n      items {\\n        ...ConsumerOrderOrderItemFragment\\n        __typename\\n      }\\n      __typename\\n    }\\n    paymentCard {\\n      ...ConsumerOrderPaymentCardFragment\\n      __typename\\n    }\\n    grandTotal {\\n      unitAmount\\n      currency\\n      decimalPlaces\\n      displayString\\n      sign\\n      __typename\\n    }\\n    likelyOosItems {\\n      menuItemId\\n      name\\n      photoUrl\\n      __typename\\n    }\\n    pollingInterval\\n    store {\\n      id\\n      name\\n      business {\\n        id\\n        name\\n        __typename\\n      }\\n      phoneNumber\\n      fulfillsOwnDeliveries\\n      customerArrivedPickupInstructions\\n      isPriceMatchingEnabled\\n      priceMatchGuaranteeInfo {\\n        headerDisplayString\\n        bodyDisplayString\\n        buttonDisplayString\\n        __typename\\n      }\\n      __typename\\n    }\\n    recurringOrderDetails {\\n      itemNames\\n      consumerId\\n      recurringOrderUpcomingOrderUuid\\n      scheduledDeliveryDate\\n      arrivalTimeDisplayString\\n      storeName\\n      isCancelled\\n      __typename\\n    }\\n    bundleOrderInfo {\\n      ...BundleOrderInfoFragment\\n      __typename\\n    }\\n    cancellationPendingRefundInfo {\\n      state\\n      originalPaymentAmount {\\n        unitAmount\\n        currency\\n        decimalPlaces\\n        displayString\\n        sign\\n        __typename\\n      }\\n      creditAmount {\\n        unitAmount\\n        currency\\n        decimalPlaces\\n        displayString\\n        sign\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment ConsumerOrderPaymentCardFragment on ConsumerOrderPaymentCard {\\n  id\\n  last4\\n  type\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemFragment on ConsumerOrderOrderItem {\\n  id\\n  name\\n  quantity\\n  specialInstructions\\n  substitutionPreferences\\n  orderItemExtras {\\n    ...ConsumerOrderOrderItemExtraFragment\\n    __typename\\n  }\\n  purchaseQuantity {\\n    ...ConsumerOrderQuantityFragment\\n    __typename\\n  }\\n  fulfillQuantity {\\n    ...ConsumerOrderQuantityFragment\\n    __typename\\n  }\\n  originalItemPrice\\n  purchaseType\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraOptionFields on OrderItemExtraOption {\\n  menuExtraOptionId\\n  name\\n  description\\n  price\\n  quantity\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraOptionFragment on OrderItemExtraOption {\\n  ...ConsumerOrderOrderItemExtraOptionFields\\n  orderItemExtras {\\n    ...ConsumerOrderOrderItemExtraFields\\n    orderItemExtraOptions {\\n      ...ConsumerOrderOrderItemExtraOptionFields\\n      orderItemExtras {\\n        ...ConsumerOrderOrderItemExtraFields\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraFields on OrderItemExtra {\\n  menuItemExtraId\\n  name\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraFragment on OrderItemExtra {\\n  ...ConsumerOrderOrderItemExtraFields\\n  orderItemExtraOptions {\\n    ...ConsumerOrderOrderItemExtraOptionFragment\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ConsumerOrderCreatorFragment on ConsumerOrderCreator {\\n  id\\n  firstName\\n  lastName\\n  __typename\\n}\\n\\nfragment ConsumerOrderQuantityFragment on Quantity {\\n  continuousQuantity {\\n    quantity\\n    unit\\n    __typename\\n  }\\n  discreteQuantity {\\n    quantity\\n    unit\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment BundleOrderInfoFragment on BundleOrderInfo {\\n  primaryBundleOrderUuid\\n  primaryBundleOrderId\\n  bundleOrderUuids\\n  bundleOrderConfig {\\n    ...BundleOrderConfigFragment\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment BundleOrderConfigFragment on BundleOrderConfig {\\n  bundleType\\n  bundleOrderRole\\n  __typename\\n}\\n"}

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
        # print("COOKIES")
        # print(cookie_str)
        # print("COOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIESCOOKIES")
        self.headers['cookie'] = cookie_str

    
    def build_curl_command(self, offset=0, limit=30, include_cancelled=True):
        self.data_template['variables']['offset'] = offset
        self.data_template['variables']['limit'] = limit
        self.data_template['variables']['includeCancelled'] = include_cancelled

        headers = ' '.join([f"-H '{k}: {v}'" for k, v in self.headers.items()])
        data = json.dumps(self.data_template, ensure_ascii=False).replace("\\\\n", "\\n")
        curl_command = f"curl '{self.base_url}' {headers} --data-raw '{data}'"
        return curl_command

"""
Main for dev testing
"""
class Main():
    def __init__(self):
        self.cb = curlBuilder("https://www.doordash.com/graphql/getConsumerOrdersWithDetails?operation=getConsumerOrdersWithDetails")
        self.cb.get_cookies()
        print(self.cb.build_curl_command(0, 30, True))

if __name__ == "__main__":
    Main()