<!-- slide -->

# Python String Formatting

<!-- slide -->

## Contents

1. String Format with `%`
2. String format with `.format`
3. f-strings
4. Template strings

<!-- slide -->

## Part 1. String Format with `%`

```Python
name = 'Matt'

print('Hello, %s' % name)
# => 'Hello, Matt'
```

Using the `%` operator for string formatting is a legacy tool - not commonly
used anymore.

<!-- slide -->

## Part 2. String format with `.format`

```Python
num = 50159747054
name = 'Matt'

print('Hello, {}'.format(name))
# => 'Hello, Matt'

print('Hey {name}, there is a 0x{num:x} error!'.format(name=name, num=num))
# => 'Hey Matt, there is a 0xbadc0ffee error!'
```

Note: the `{num:x}` means to format it as hex.

<!-- slide -->

## Part 3. f-strings

<!-- slide -->

## Part 4. Template strings
