import colander


class FKMapping(colander.MappingSchema):
    """A Foreign key Mapping between a external and internal id"""
    external_fk = colander.SchemaNode(colander.String())
    internal_value = colander.SchemaNode(colander.String())
    pattern = colander.SchemaNode(colander.String(), missing='pk')


class FKMappings(colander.SequenceSchema):
    """Collection of foreign keys mapping"""
    fkmapping = FKMapping()


class Field(colander.MappingSchema):
    """A field represented by our external/internal name and a foreign keys mapping"""
    external_name = colander.SchemaNode(colander.String())
    model_name = colander.SchemaNode(colander.String())
    foreign_key_mapping = FKMappings()


class Fields(colander.SequenceSchema):
    """A collection of fields"""
    field = Field()
