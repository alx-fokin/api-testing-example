"""This module contains set of xsd schemas for xml response validation."""

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
