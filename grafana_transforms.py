# -*- coding: utf-8 -*-
"""Grafana panel transformation builders mapped from dashboard YAML definitions."""


class Transformation:
    """Base class for Grafana transformations."""

    def __init__(self, id, options=None):  # pylint: disable=redefined-builtin
        """Initialize a transformation with its Grafana identifier and options dict."""
        self.id = id
        self.options = options if options is not None else {}

    def to_json_data(self):
        """Return the JSON structure for the transformation."""
        return {
            'id': self.id,
            'options': self.options,
        }


# --- Filtering and Selection Transformations ---


class FilterByName(Transformation):
    """Filter fields by their name."""

    def __init__(self, include=None):
        """Include only fields matching the given names."""
        options = {
            "include": {"names": include}
        }
        super().__init__('filterFieldsByName', options)


class FilterByValue(Transformation):
    """Filter data rows based on field values."""

    def __init__(self, field, operator, value):
        """Filter records where `field` satisfies `operator` against `value`."""
        options = {
            "filters": [
                {
                    "fieldName": field,
                    "config": {
                        "id": f"filter-by-value-{field}",
                        "options": {
                            "operator": operator,
                            "value": value
                        }
                    }
                }
            ]
        }
        super().__init__('filterByValue', options)


class FilterByQuery(Transformation):
    """Show or hide query results by query refId."""

    def __init__(self, refIds):
        """Keep data frames matching the specified query refIds."""
        options = {
            "refIds": refIds
        }
        super().__init__('filterByRefId', options)


# --- Combining Transformations ---


class Merge(Transformation):
    """Merge results from multiple queries into one frame."""

    def __init__(self):
        """Initialize a merge transformation."""
        super().__init__('merge')


class OuterJoin(Transformation):
    """Join multiple time series on a shared label field."""

    def __init__(self, field):
        """Join series frames by the specified field name."""
        options = {
            "join": field
        }
        super().__init__('outerJoin', options)


# --- Calculation and Aggregation Transformations ---


class AddFieldFromCalculation(Transformation):
    """Create a computed field from an arithmetic or reduced expression."""

    def __init__(self, mode, reducer, expression=None):
        """Initialize a calculated field transformation."""
        options = {
            'mode': mode,
            'reducer': reducer,
        }
        if expression:
            options['expression'] = expression
        super().__init__('addFieldFromCalculation', options)


class Reduce(Transformation):
    """Reduce each series to a single summary value."""

    def __init__(self, reducer):
        """Apply the specified reducer to collapse time series rows."""
        options = {
            "reducers": [reducer]
        }
        super().__init__('reduce', options)


class GroupBy(Transformation):
    """Group rows by labels and aggregate remaining columns."""

    def __init__(self, fields, aggregations):
        """Group frames on `fields` using `aggregations` rules."""
        options = {
            "fields": fields,
            "aggregations": aggregations
        }
        super().__init__('groupBy', options)


# --- Formatting and Renaming Transformations ---


class Organize(Transformation):
    """Reorder, rename, or hide columns."""

    def __init__(self, renameByName=None, sortBy=None):
        """Configure optional field rename mappings and display ordering."""
        options = {}
        if renameByName:
            options["renameByName"] = renameByName
        if sortBy:
            options["sortBy"] = sortBy
        super().__init__('organize', options)


class LabelsToFields(Transformation):
    """Extract Prometheus labels into dedicated table columns."""

    def __init__(self, labels=None, valueLabel=None):
        """Convert selected metric labels into fields."""
        options = {}
        if labels:
            options['labels'] = labels
        if valueLabel:
            options['valueLabel'] = valueLabel
        super().__init__('labelsToFields', options)


class SeriesToRows(Transformation):
    """Combine multiple time series into a single tabular view."""

    def __init__(self):
        """Initialize a series-to-rows transformation."""
        super().__init__('seriesToRows')


class ConvertFieldType(Transformation):
    """Convert the data type of a target field."""

    def __init__(self, field, targetType):
        """Cast `field` to `targetType`."""
        options = {
            'field': field,
            'targetType': targetType
        }
        super().__init__('convertFieldType', options)


class GroupToNestedTable(Transformation):
    """Group matching rows into nested sub-tables."""

    def __init__(self, key):
        """Nest rows grouped by `key`."""
        options = {
            'key': key
        }
        super().__init__('groupToNestedTable', options)


# --- Specific Transformations ---


class SortBy(Transformation):
    """Sort rows by the value of a specified field."""

    def __init__(self, field, reverse=False):
        """Sort frames by `field` ascending or descending."""
        options = {
            'sort': [
                {
                    'field': field,
                    'reverse': reverse
                }
            ]
        }
        super().__init__('sortBy', options)


class Limit(Transformation):
    """Limit the maximum number of displayed rows."""

    def __init__(self, limit):
        """Cap output rows at `limit`."""
        options = {
            'limit': limit
        }
        super().__init__('limit', options)


class ExtractFields(Transformation):
    """Extract structured values from a field using a regular expression."""

    def __init__(self, source, regex, rename=None):
        """Parse `source` field values using `regex` and optional `rename` mapping."""
        options = {
            'source': source,
            'regex': regex
        }
        if rename:
            options['rename'] = rename
        super().__init__('extractFields', options)


class Debug(Transformation):
    """Display transformation frame output for debugging."""

    def __init__(self):
        """Initialize a Grafana debug transformation."""
        super().__init__('debug')


# Mapping from YAML transformation type names to Python builder classes.
TRANSFORMATIONS_MAP = {
    'filterByName': FilterByName,
    'filterByValue': FilterByValue,
    'filterByQuery': FilterByQuery,
    'merge': Merge,
    'outerJoin': OuterJoin,
    'addFieldFromCalculation': AddFieldFromCalculation,
    'reduce': Reduce,
    'groupBy': GroupBy,
    'organize': Organize,
    'labelsToFields': LabelsToFields,
    'seriesToRows': SeriesToRows,
    'convertFieldType': ConvertFieldType,
    'groupToNestedTable': GroupToNestedTable,
    'sortBy': SortBy,
    'limit': Limit,
    'extractFields': ExtractFields,
    'debug': Debug,
}
