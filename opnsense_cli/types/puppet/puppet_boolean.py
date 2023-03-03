from opnsense_cli.types.puppet.base import PuppetCodeFragment


class PuppetBoolean(PuppetCodeFragment):
    TEMPLATE_PROVIDER_translate_json_object_to_puppet_resource = '''
    ${name}: bool_from_value(json_object['${name}']),
    '''

    TEMPLATE_PROVIDER_translate_puppet_resource_to_command_args = '''
    args.push('--${name}') if bool_from_value(puppet_resource[:${name}]) == true
            args.push('--no-${name}') if bool_from_value(puppet_resource[:${name}]) == false
    '''

    TEMPLATE_TYPE_example = '''
    ${name} => TODO,
    '''

    TEMPLATE_TYPE_attributes = '''
    ${name}: {
          type: 'Boolean',
          desc: '${help}',
        },
    '''

    TEMPLATE_TYPE_attributes_namevar = '''
    ${name}: {
          type: 'Boolean',
          desc: '${help}',
          behaviour: :namevar,
        },
    '''
