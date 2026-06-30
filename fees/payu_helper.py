import hashlib

def generate_payu_hash(params, salt):
    hash_str = (
        f"{params.get('key', '')}|"
        f"{params.get('txnid', '')}|"
        f"{params.get('amount', '')}|"
        f"{params.get('productinfo', '')}|"
        f"{params.get('firstname', '')}|"
        f"{params.get('email', '')}|"
        f"{params.get('udf1', '')}|"
        f"{params.get('udf2', '')}|"
        f"{params.get('udf3', '')}|"
        f"{params.get('udf4', '')}|"
        f"{params.get('udf5', '')}|"
        f"|||||"
        f"{salt}"
    )
    return hashlib.sha512(hash_str.encode('utf-8')).hexdigest()

def verify_payu_hash(response_data, salt):
    """
    Reverse hash for response verification:
    sha512(salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key)
    """
    hash_sequence = [
        salt,
        response_data.get('status', ''),
        '',  # udf10
        '',  # udf9
        '',  # udf8
        '',  # udf7
        '',  # udf6
        response_data.get('udf5', ''),
        response_data.get('udf4', ''),
        response_data.get('udf3', ''),
        response_data.get('udf2', ''),
        response_data.get('udf1', ''),
        response_data.get('email', ''),
        response_data.get('firstname', ''),
        response_data.get('productinfo', ''),
        response_data.get('amount', ''),
        response_data.get('txnid', ''),
        response_data.get('key', ''),
    ]
    hash_str = '|'.join(hash_sequence)
    return hashlib.sha512(hash_str.encode('utf-8')).hexdigest()