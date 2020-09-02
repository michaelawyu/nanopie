# Data Models

nanopie provides a `Model` class which you can inherit from to model
data in their microservices and API backends. Each `Model` may include
a number of `Fields` as attributes, which describe the data. With the
help of Python metaclasses
([PEP 3115](https://www.python.org/dev/peps/pep-3115/)), nanopie automatically
adds to data model classes initializers and properties corresponding
to the `Fields` you provide; you may then use instances of your data model
classes in the same way as regular data classes.

``` python
from nanopie import Model, StringField, IntField

class User(Model):
    name = StringField()
    age = IntField()

user = User(name="Albert Wesker", age=49)
# Returns "Albert Wesker"
print(user.name)
# Returns 49
print(user.age)
```

In addition, you may specify a number of hints and constraints with each
`Field`; nanopie can validate data against them automatically for you.
The snippet below, for example, specifies a `StringField` whose value
must have only alphabetic characters with a length of no less than 1
character and no more than 20 characters.

``` python
from nanopie import Model

class User(Model):
    name = StringField(max_length=20, min_length=1, pattern="^[a-zA-Z]$")

# These statements will raise an exception
user = User(name="#wesker")
user = User(name="")
user = User(name="SuperUltraMegaLongName")

user = User(name="Wesker")
# This will also raise an exception
user.name = ""
```

## Fields

nanopie provides the following fields:

* `StringField`: A field for string (`str`) typed data.
* `IntField`: A field for integer (`int`) typed data.
* `FloatField`: A field for float (`float`) typed data.
* `BoolField`: A field for boolean (`bool`) typed data.
* `ArrayField`: A field for array (`List`) typed data.
* `ObjectField`: A field for object typed data. This field allows you to nest
a data model within another data model.

### `StringField`

To add a field for string typed data in your data model, specify a
`StringField` as attribute in your `Model` class. This field supports
the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`format`  | The format of this field. For example, a `StringField` for timstamps may have its `format` set to `date-time`. This field is informational, i.e. nanopie will not be able to validate if the value of a `StringField` matches its `format`.
`max_length`  | The maximum length of this field, e.g. `20`.
`min_length`  | The minimum length of this field, e.g. `1`.
`pattern`  | The pattern of this field, in the form of a regular expression. A `StringField`, for example, with a `pattern` of `^[a-z]*$` will only accept strings with lower case alphabetic characters.
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None` (an empty string, `""`, however is still valid).
`default`  | The default value of this field.
`description` | The description of this field.

``` python
class UserCredential(Model):
    password = StringField(format="password",
                           max_length=16,
                           min_length=8,
                           pattern='[a-zA-Z0-9]^$',
                           required=True,
                           default='00000000',
                           description='An example StringField')
```

### `IntField`

To add a field for integer typed data in your data model, specify an
`IntField` as attribute in your `Model` class. This field supports
the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`maximum`  | The maximum value of this field.
`exclusive_maximum`  | Defaults to `False`; if set to `True`, the maximum value itself will be excluded. For example, if an `IntField` has `maximum` set to `20` and `exclusive_maximum` to `True`, `20` itself will not be a valid value for this field and the largest value this field can take will be `19` (`<` instead of `<=`).
`minimum`  | The minimum value of this field.
`exclusive_minimum`  | Defaults to `False`; if set to `True`, the minimum value itself will be excluded. For example, if an `IntField` has `minimum` set to `1` and `exclusive_maximum` to `True`, `1` itself will not be a valid value for this field and the smallest value this field can take will be `2` (`>` instead of `>=`).
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None`.
`default`  | The default value of this field.
`description` | The description of this field.

``` python
class User(Model):
    age = IntField(maximum=150,
                   exclusive_maximum=False,
                   minimum=0,
                   exclusive_minimum=False,
                   default=0,
                   required=True,
                   description="An example IntField")
```

### `FloatField`

To add a field for float typed data in your data model, specify an
`FolatField` as attribute in your `Model` class. This field supports
the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`maximum`  | The maximum value of this field.
`exclusive_maximum`  | Defaults to `False`; if set to `True`, the maximum value itself will be excluded. For example, if a `FloattField` has `maximum` set to `20.0` and `exclusive_maximum` to `True`, `20.0` itself will not be a valid value for this field (`<` instead of `<=`).
`minimum`  | The minimum value of this field.
`exclusive_minimum`  | Defaults to `False`; if set to `True`, the minimum value itself will be excluded. For example, if a `FloatField` has `minimum` set to `1.0` and `exclusive_maximum` to `True`, `1.0` itself will not be a valid value for this field (`>` instead of `>=`).
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None`.
`default`  | The default value of this field.
`description` | The description of this field.

``` python
class NewTempatureReadingEvent(Model):
    temperature = FloatField(maximum=100.0,
                             exclusive_maximum=False,
                             minimum=0.0,
                             exclusive_minimum=False,
                             default=0.0,
                             required=True,
                             description="An example FloatField")
```

### `BoolField`

To add a field for boolean typed data in your data model, specify a
`BoolField` as attribute in your `Model` class. This field supports
the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None`.
`default`  | The default value of this field.
`description` | The description of this field.

``` python
class User(Model):
    is_subscriber = BoolField(required=True,
                              default=False,
                              description="An example BoolField")
```

### `ArrayField`

To add a field for array (list) typed data in your data model, specify
an `ArrayField` as attribute in your `Model` class. You must specify
the type of the items of the array in the form of a `Field` along with the
`ArrayField` itself. The code snippet below includes an `ArrayField`
that accepts an array (list) of integers:

``` python
class Order(Model):
    item_ids = ArrayField(
        item_field=IntField(required=True)
    )
```

!!! note
    nanopie will use the hints and constraints specified in the item field (if
    any) to validate each item in the array.

`ArrayField` supports the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`item_field` | **Required**. A field that describes the items in the array (list).
`min_items` | The minimum number of items in the array.
`max_items` | The maximum number of items in the array.
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None`.
`default`  | The default value of this field.
`description` | The description of this field.

### `ObjectField`

`ObjectField` allows you to specify object typed data in your data model. It
effectively nests a data model within another. Each `ObjectField` requires a
`Model` class as argument, which describes what the object typed data looks
like. The code snippet below includes an `ObjectField` that uses the `Address`
data model and accepts an instance of the `Address` model as value:

``` python
class Address(Model):
    address_line_1 = StringField()
    address_line_2 = StringField()
    city = StringField()
    state_or_province = StringField()
    country_or_region = StringField()

class User(Model):
    name = StringField()
    address = ObjectField(model=Address)

user = User(
    name = "Albert Wesker",
    address = Address(address_line_1="Captain's office, STARS, Racoon City Police Dept.",
                      city="Racoon City",
                      state_or_province="MI",
                      country="US")
)

# Returns "Captain's office, STARS, Racoon City Police Dept."
print(user.address.address_line_1)
```

`ObjectField` supports the following hints and constraints:

Hint/Constraint  | Description
------------- | -------------
`model` | **Required**. A data model that describes the object.
`required`  | Defaults to `False`; if set to `True`, this field is required in a model, i.e. its value cannot be `None`.
`default`  | The default value of this field.
`description` | The description of this field.

## Using Models

When you define a `Model` with a number of `Fields`, nanopie sets up these
`Fields` as properties with getters and setters; it also configures an
initializer for the `Model` class.

You can instantiate a `Model` using its initializer by passing the values
of fields as keyword arguments. The initializer will validate these values
against the hints and constraints in their fields. Fields that are not listed
in the given keyword arguments will be assigned its default value 
(if specified) or `None`. Note that if a field is required but assigned
the value of `None`, an exception will be thrown.

If you would like to skip the validation process, set the argument
`skip_validation` to `True` when calling the initializer:

``` python
from nanopie import Model, StringField

class User(Model):
    name = StringField(required=True)

# An exception will be raised, as the required field, `name`, is not assigned
# a value
user = User()

# No exception will be raised
user = User(skip_validation=True)
# Returns None
print(user.name)
```

Once instantiated, you may update the values of fields with getters and 
setters. Note that when you assigned a value to a field, nanopie will
automatically validate the input against the hints and constraints (if any)
specified in the corresponding field.

The `Model` class also features some utility methods you can use, including

Method  | Type | Description
------------- | ------------- | -------------
`from_dikt`  | Class method | Parses a `Dict` into a data model instance
`to_dikt` | Instance method | Dumps a data model instance into a `Dict`.
`validate` | Instance method | Validates the data model instance against its data model.
`validate_instance` | Class method | Validates any data model instance against the data model.

## Exceptions

When a validation fails, nanopie will throw exceptions of the following classes;
you may catch them and process the validation exceptions properly. All of the
classes below inherit from the `nanopie.misc.errors.ValidationError` class (which is in turn based on the `nanopie.misc.errors.ServiceError` class).

Exception | Description | Field-specific Exception
------------- | ------------- | ----------------------
`ModelTypeNotMatchedError` | This exception is raised when the input data is of a data model different from the one used for validation. | No
`RequiredFieldMissingError` | This exception is raised when a missing field is missing (not assigned a value or assigned the value of `None`). | Yes
`FieldTypeNotMatchedError` | This exception is raised when a field is assigned a value not matching its associated data type. | Yes
`ListItemTypeNotMatchedError` | This exception is raised when an `ArrayField` is assigned a list in which one or more items does not match the field's associated item data type. | Yes
`StringMaxLengthExceededError` | This exception is raised when a `StringField` is assigned a value that is too long. | Yes
`StringMinLengthBelowError` | This exception is raised when a `StringField` is assigned a value that is too short. | Yes
`StringPatternNotMatchedError` | This exception is raised when a `StringField` is assigned a value that is not of the specified pattern. | Yes
`NumberMaxExceededError` | This exception is raised when an `IntField` or a `FloatField` is assigned a value that is too large. | Yes
`NumberMinBelowError` | This exception is raised when an `IntField` or a `FloatField` is assigned a value that is too small. | Yes
`ListTooManyItemsError` | This exception is raised when an `ArrayField` is assigned a list that has too many items. | Yes
`ListTooLittleItemsError` | This exception is raised when an `ArrayField` is assigned a list that has too little items. | Yes

Each exception has 4 attributes:

* `source`: The source data field or model.
* `data`: The value assigned to the field or model that triggers the exception.
* `message`: The error message.
* `response`: The RPC response associated with the exception. Defaults to `None`.

If the exception is field specific, it will also include the name of the field
in the data model, `assigned_field_name`, as an attribute.

!!! note
    Learn more about nanopie exceptions in [Exceptions](/exceptions).
