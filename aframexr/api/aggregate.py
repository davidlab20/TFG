"""AframeXR aggregate."""

from pandas import DataFrame

from aframexr.utils.validators import AframeXRValidator


class AggregatedFieldDef:
    """Aggregated field definition."""

    def __init__(self, op: str, field: str, as_field: str = ''):
        AframeXRValidator.validate_aggregate_operation(op)
        self.op = op

        if op != 'count' and not field:  # Field must be filled except using "count" operation
            raise ValueError(f'Parameter "field" cannot be empty using {op}.')
        self.field = field

        if not as_field:
            as_field = field
        self.as_field = as_field

    # Import
    @staticmethod
    def from_dict(aggregate_specs: dict):
        """Creates an AggregatedFieldDef object from the aggregate specifications."""

        AframeXRValidator.validate_type(aggregate_specs, dict)

        try:  # Validate that 'field' and 'aggregate' are ono the specifications
            aggregate_op = aggregate_specs['op']
            field = aggregate_specs['field']
            as_field = aggregate_specs.get('as', field)
        except KeyError:
            raise KeyError('Invalid aggregate specification, must contain "op" and "field".')
        return AggregatedFieldDef(aggregate_op, field, as_field)

    # Export
    def to_dict(self) -> dict:
        """Returns the dictionary representation for chart specifications of the aggregated field."""

        specs: dict = {'op': self.op, 'field': self.field}
        if self.as_field:
            specs['as'] = self.as_field
        return specs

    # Utils
    def get_aggregated_data(self, data: DataFrame, groupby: list) -> DataFrame:
        """Returns the aggregated data."""

        try:
            agg_map = {self.as_field: (self.field, self.op)}
            aggregated_data = data.groupby(groupby).agg(**agg_map).reset_index()
        except KeyError as e:
            unknown_fields = e.args[0]  # Fields that are not in data
            raise KeyError(f'Data has no key {unknown_fields}.')
        return aggregated_data

    @staticmethod
    def split_operator_field(aggregate_formula: str):
        """Returns the aggregate operator, the field and the groupby in the aggregate formula."""

        field, aggregate_op = aggregate_formula, None

        if '(' in aggregate_formula and  ')' in aggregate_formula:
            aggregate_op = aggregate_formula.split('(')[0].strip()  # Value before parentheses (aggregate operation)
            AframeXRValidator.validate_aggregate_operation(aggregate_op)  # Validate that the aggregate is correct

            field = aggregate_formula.split('(')[1].split(')')[0].strip()  # Value between parentheses (field)
        return field, aggregate_op
