"""This module contains set of informational messages templates."""

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
