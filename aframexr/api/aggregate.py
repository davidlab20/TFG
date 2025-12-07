"""AframeXR aggregate."""

from pandas import DataFrame

from aframexr.utils.validators import AframeXRValidator


class AggregatedFieldDef:
    """Aggregated field definition."""

    def __init__(self, op: str, field: str, encoding_type: str | None = None, group_by: str | None = None):
        self.op = op
        self.field = field
        self.encoding_type = encoding_type
        self.group_by = group_by

    # Import
    @staticmethod
    def from_dict(aggregate_specs: dict):
        """Creates an AggregatedFieldDef object from the aggregate specifications."""

        AframeXRValidator.validate_type(aggregate_specs, dict)

        try:  # Validate that 'field' and 'aggregate' are ono the specifications
            field = aggregate_specs['field']
            aggregate_op = aggregate_specs['aggregate']
        except KeyError:
            raise ValueError('Invalid aggregate specification, must contain "field" and "aggregate".')
        encoding_type = aggregate_specs.get('type')  # Could not be in the aggregate specifications
        group_by = aggregate_specs.get('group_by')  # Could not be in the aggregate specifications
        return AggregatedFieldDef(aggregate_op, field, encoding_type, group_by)

    # Export
    def to_dict(self) -> dict:
        """Returns the dictionary representation for chart specifications of the aggregated field."""

        specs = {'field': self.field, 'aggregate': self.op}
        if self.encoding_type:
            specs.update({'type': self.encoding_type})
        if self.group_by:
            specs.update({'group_by': self.group_by})
        return specs

    # Utils
    def aggregate_data(self, data: list[dict]) -> DataFrame:
        """Returns the aggregated data."""

        pass

    @staticmethod
    def split_operator_field_groupby(aggregate_formula: str):
        """Returns the aggregate operator, the field and the group_by in the aggregate formula."""

        field, aggregate_op, group_by = aggregate_formula, None, None

        if '(' in aggregate_formula and  ')' in aggregate_formula:
            aggregate_op = aggregate_formula.split('(')[0].strip()  # Value before parentheses (aggregate operation)
            AframeXRValidator.validate_aggregate_operation(aggregate_op)  # Validate that the aggregate is correct

            field_groupby = aggregate_formula.split('(')[1].split(')')[0].strip()  # Value between parentheses (field)
            field_groupby = field_groupby.split(',')
            try:
                field = field_groupby[0].strip()
                group_by = field_groupby[1].strip()
            except IndexError:
                field = field_groupby[0]

        return field, aggregate_op, group_by
