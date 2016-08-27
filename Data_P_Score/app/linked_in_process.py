import requests

url = 'https://api.linkedin.com/v1/people/~'
headers = {'host':'api.linkedin.com','content-type': 'application/x-www-form-urlencoded','connection':'Keep-Alive','authorization':'Bearer AQV92YV966l9kriDnqHL_vWHvHGIrEoqTOROW8Pk9n0oVIzYrUYCPW-23NFQ_N3B8sf-KQaPVdZ1aIRdkaLcepFTf1n-A2P4FZK4DDNQc1NS_GMgBMKO3t3SdqdiOhAK34W1axGN29t_sxLHyfrXQAlEvvpqaeM3vRBkXgrBaYYlyr_Mas0'}
params = {'grant_type':'authorization_code','code':'AQQvSpVCgJJqbgTE0WgNR32VcddMwo6LCawwz5BQ2QdvTnD1nEmsJNI3zfAIYvf3X_PuAD9y95hfZWIcFI7iN5DTZw1GeuZmph1lRBWKhpwGojn58z8','redirect_uri':'http://localhost:5000','client_id':'783ishqqzfo4ug','client_secret':'YuFs0VNr7LuoravI'}

r = requests.get(url, headers=headers, data=params)

print r.text

    # https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=783ishqqzfo4ug&redirect_uri=http%3A//localhost%3A5000&state=06215719

    # code=AQTAI7rauxOPuTkgRPAMrHihS3JpAJIFv8YK7kJBjH35tk3K-eVXdZHhweeTtyy27EqVaRE9jmxbcDfYCQZkYFjsp-Q6oYm2ryQTT5aClsaTvM_dL4s&state=06215719
    # data = {'grant_type':'authorization_code','code':'AQTAI7rauxOPuTkgRPAMrHihS3JpAJIFv8YK7kJBjH35tk3K-eVXdZHhweeTtyy27EqVaRE9jmxbcDfYCQZkYFjsp-Q6oYm2ryQTT5aClsaTvM_dL4s','redirect_uri':'http%3A//localhost%3A5000','client_id':'783ishqqzfo4ug','client_secret':'YuFs0VNr7LuoravI'}
    # code=AQQvSpVCgJJqbgTE0WgNR32VcddMwo6LCawwz5BQ2QdvTnD1nEmsJNI3zfAIYvf3X_PuAD9y95hfZWIcFI7iN5DTZw1GeuZmph1lRBWKhpwGojn58z8&state=06215719