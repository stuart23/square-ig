from .tenant_client import TenantClient


def test__generate_dynamo_update_props():
    args = {'abc': 123, 'def': 456, 'ghi': 'hello', 'jkl': 'goodbye'}
    result = TenantClient._generate_dynamo_update_props(args)
    assert 'UpdateExpression' in result.keys()
    assert 'ExpressionAttributeValues' in result.keys()
    assert result['UpdateExpression'] == \
        'set abc=:abc, def=:def, ghi=:ghi, jkl=:jkl'
    assert result['ExpressionAttributeValues'] == {
        ':abc': 123, ':def': 456, ':ghi': 'hello', ':jkl': 'goodbye'
    }