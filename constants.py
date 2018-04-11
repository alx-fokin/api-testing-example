# URL TEMPLATES SECTION
verify_url = 'https://api.nexmo.com/verify/{}?api_key={}&' \
             'api_secret={}&brand={}&number={}'
check_url = 'https://api.nexmo.com/verify/check/{}?api_key={}&' \
            'api_secret={}&request_id={}&code={}'
control_url = 'https://api.nexmo.com/verify/control/{}?api_key={}&' \
              'api_secret={}&request_id={}&cmd={}'
search_url = 'https://api.nexmo.com/verify/search/{}?api_key={}&' \
             'api_secret={}'
balance_url = 'https://rest.nexmo.com/account/get-balance?api_key={}&api_secret={}'
verify_url_without_apikey = 'https://api.nexmo.com/verify/{}?' \
                            'api_secret={}&brand={}&number={}'
verify_url_without_apisecret = 'https://api.nexmo.com/verify/{}?api_key={}&' \
                               'brand={}&number={}'

# MESSAGES SECTION
code_does_not_match_msg = 'The code provided does not match the expected value'
workflow_terminated_msg = 'A wrong code was provided too many times. Workflow terminated'
request_cannot_be_cancelled_msg = 'Verification request [\'{}\'] can\'t be cancelled ' \
                                  'within the first 30 seconds.'
request_not_exist_or_active_msg = 'The requestId \'{}\' does not exist or its no longer active.'
request_not_found_or_verified_msg = 'The Nexmo platform was unable to process this message for ' \
                                    'the following reason: Request \'{}\' was not found or it ' \
                                    'has been verified already.'
no_more_event_to_execute_msg = 'No more events are left to execute for the request [\'{}\']'
concurrent_verifications_msg = 'Concurrent verifications to the same number are not allowed'
invalid_value_msg = 'Invalid value for param: {}'
missing_apikey_msg = 'Missing api_key'
missing_mandatory_parms_msg = 'Your request is incomplete and missing some mandatory parameters'
bad_credentials_msg = 'Bad Credentials'
missing_specific_mandatory_parm_msg = 'Your request is incomplete and missing the mandatory parameter: {}'
parameter_is_too_long_msg = 'Invalid value for param: {}. Parameter is too long.'
allowed_code_length_values_msg = 'Invalid value for param: code_length. The allowed values are 4 and 6.'
code_invalid_characters_msg = 'The code contains invalid characters'
invalid_parameter_found_msg = 'Invalid parameter found: {}'
no_response_found_msg = 'No response found'

# JSON SCHEMAS SECTION
verify_search_requestid_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "request_id": {
            "type": "string",
            "maxLength": 32
        },
        "account_id": {
            "type": "string"
        },
        "number": {
            "type": "string"
        },
        "sender_id": {
            "type": "string"
        },
        "date_submitted": {
            "format": "date-time",
            "type": "string"
        },
        "date_finalized": {
            "format": "date-time",
            "type": "string"
        },
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date_received": {
                        "format": "date-time",
                        "type": "string"
                    },
                    "code": {
                        "format": "date-time",
                        "type": "string"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["VALID", "INVALID"]
                    },
                    "ip_address": {
                        "format": "date-time",
                        "type": "string"
                    }
                },
                'additionalProperties': False,
            }
        },
        "first_event_date": {
            "type": "string"
        },
        "last_event_date": {
            "type": "string"
        },
        "price": {
            "type": "string"
        },
        "currency": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["IN PROGRESS", "SUCCESS", "FAILED", "EXPIRED", "CANCELLED"]
        }
    },
    "required": [
        "request_id",
        "account_id",
        "number",
        "sender_id",
        "date_submitted",
        "date_finalized",
        "checks",
        "first_event_date",
        "last_event_date",
        "price",
        "currency",
        "status"
    ],
    "additionalProperties": False,
}

verify_search_requestids_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "verification_requests": {
            "type": "array",
            "items": verify_search_requestid_schema
        }
    },
    "required": ["verification_requests"],
    "additionalProperties": False,
}

# XML SCHEMA SECTION
verify_search_requestid_xsd_schema = '''<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" 
xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="verify_request">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="request_id" minOccurs="1" maxOccurs="1">
          <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:maxLength value="50" />
            </xs:restriction>
          </xs:simpleType>
        </xs:element>
        <xs:element type="xs:string" name="account_id" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="number" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="sender_id" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="date_submitted" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="date_finalized" minOccurs="1" maxOccurs="1"/>
        <xs:element name="checks">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="check" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                  <xs:sequence>
                    <xs:element type="xs:string" name="date_received" minOccurs="1" maxOccurs="1"/>
                    <xs:element type="xs:string" name="code" minOccurs="1" maxOccurs="1"/>
                    <xs:element name="status" minOccurs="1" maxOccurs="1">
                        <xs:simpleType>
                            <xs:restriction base="xs:string">
                                <xs:enumeration value="VALID"/>
                                <xs:enumeration value="INVALID"/>
                            </xs:restriction>
                        </xs:simpleType>
                    </xs:element>  
                    <xs:element type="xs:string" name="ip_address" minOccurs="1" maxOccurs="1"/>
                  </xs:sequence>
                </xs:complexType>
              </xs:element>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element type="xs:string" name="first_event_date" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="last_event_date" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="price" minOccurs="1" maxOccurs="1"/>
        <xs:element type="xs:string" name="currency" minOccurs="1" maxOccurs="1"/>
        <xs:element name="status" minOccurs="1" maxOccurs="1">
            <xs:simpleType>
                <xs:restriction base="xs:string">
                    <xs:enumeration value="IN PROGRESS"/>
                    <xs:enumeration value="SUCCESS"/>
                    <xs:enumeration value="FAILED"/>
                    <xs:enumeration value="EXPIRED"/>
                    <xs:enumeration value="CANCELLED"/>
                </xs:restriction>
            </xs:simpleType>
        </xs:element>    
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>'''


verify_search_requestids_xsd_schema = '''<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" 
xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="verification_requests">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="verify_request" maxOccurs="unbounded" minOccurs="1">
          <xs:complexType>
              <xs:sequence>
                <xs:element name="request_id" minOccurs="1" maxOccurs="1">
                  <xs:simpleType>
                    <xs:restriction base="xs:string">
                        <xs:maxLength value="50" />
                    </xs:restriction>
                  </xs:simpleType>
                </xs:element>
                <xs:element type="xs:string" name="account_id" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="number" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="sender_id" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="date_submitted" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="date_finalized" minOccurs="1" maxOccurs="1"/>
                <xs:element name="checks">
                  <xs:complexType>
                    <xs:sequence>
                      <xs:element name="check" maxOccurs="unbounded" minOccurs="0">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element type="xs:string" name="date_received" minOccurs="1" maxOccurs="1"/>
                            <xs:element type="xs:string" name="code" minOccurs="1" maxOccurs="1"/>
                            <xs:element name="status" minOccurs="1" maxOccurs="1">
                                <xs:simpleType>
                                    <xs:restriction base="xs:string">
                                        <xs:enumeration value="VALID"/>
                                        <xs:enumeration value="INVALID"/>
                                    </xs:restriction>
                                </xs:simpleType>
                            </xs:element>  
                            <xs:element type="xs:string" name="ip_address" minOccurs="1" maxOccurs="1"/>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                    </xs:sequence>
                  </xs:complexType>
                </xs:element>
                <xs:element type="xs:string" name="first_event_date" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="last_event_date" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="price" minOccurs="1" maxOccurs="1"/>
                <xs:element type="xs:string" name="currency" minOccurs="1" maxOccurs="1"/>
                <xs:element name="status" minOccurs="1" maxOccurs="1">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <xs:enumeration value="IN PROGRESS"/>
                            <xs:enumeration value="SUCCESS"/>
                            <xs:enumeration value="FAILED"/>
                            <xs:enumeration value="EXPIRED"/>
                            <xs:enumeration value="CANCELLED"/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>    
              </xs:sequence>
            </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
'''
