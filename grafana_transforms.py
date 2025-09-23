# -*- coding: utf-8 -*-

class Transformation:
    """Base class for Grafana transformations."""
    def __init__(self, id, options=None):
        self.id = id
        self.options = options if options is not None else {}

    def to_json_data(self):
        """Returns the JSON structure for the transformation."""
        return {
            'id': self.id,
            'options': self.options,
        }

# --- Transformations de Filtrage et Sélection ---

class FilterByName(Transformation):
    """Filters fields by their name."""
    def __init__(self, include=None):
        options = {
            "include": {"names": include}
        }
        super().__init__('filterFieldsByName', options)

class FilterByValue(Transformation):
    """Filtre les données en fonction des valeurs."""
    def __init__(self, field, operator, value):
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
    """Masque ou affiche des requêtes."""
    def __init__(self, refIds):
        options = {
            "refIds": refIds
        }
        super().__init__('filterByRefId', options)


# --- Transformations de Combinaison ---

class Merge(Transformation):
    """Fusionne les résultats de plusieurs requêtes."""
    def __init__(self):
        super().__init__('merge')

class OuterJoin(Transformation):
    """Joint plusieurs séries temporelles sur un label commun."""
    def __init__(self, field):
        options = {
            "join": field
        }
        super().__init__('outerJoin', options)


# --- Transformations de Calcul et d'Agrégation ---

class AddFieldFromCalculation(Transformation):
    """Crée un champ à partir d'un calcul."""
    def __init__(self, mode, reducer, expression=None):
        options = {
            'mode': mode,
            'reducer': reducer,
        }
        if expression:
            options['expression'] = expression
        super().__init__('addFieldFromCalculation', options)

class Reduce(Transformation):
    """Réduit une série de données à une valeur unique."""
    def __init__(self, reducer):
        options = {
            "reducers": [reducer]
        }
        super().__init__('reduce', options)

class GroupBy(Transformation):
    """Regroupe les données par labels et effectue une agrégation."""
    def __init__(self, fields, aggregations):
        options = {
            "fields": fields,
            "aggregations": aggregations
        }
        super().__init__('groupBy', options)


# --- Transformations de Formatage et Renommage ---

class Organize(Transformation):
    """Réorganise, renomme ou cache les champs."""
    def __init__(self, renameByName=None, sortBy=None):
        options = {}
        if renameByName:
            options["renameByName"] = renameByName
        if sortBy:
            options["sortBy"] = sortBy
        super().__init__('organize', options)

class LabelsToFields(Transformation):
    """Extrait les labels Prometheus pour les transformer en champs."""
    def __init__(self, labels=None, valueLabel=None):
        options = {}
        if labels:
            options['labels'] = labels
        if valueLabel:
            options['valueLabel'] = valueLabel
        super().__init__('labelsToFields', options)

class SeriesToRows(Transformation):
    """Transforme plusieurs séries temporelles en une seule table."""
    def __init__(self):
        super().__init__('seriesToRows')

class ConvertFieldType(Transformation):
    """Change le type de données d'un champ."""
    def __init__(self, field, targetType):
        options = {
            'field': field,
            'targetType': targetType
        }
        super().__init__('convertFieldType', options)

class GroupToNestedTable(Transformation):
    """Regroupe les lignes dans une table imbriquée."""
    def __init__(self, key):
        options = {
            'key': key
        }
        super().__init__('groupToNestedTable', options)

# --- Transformations Spécifiques ---

class SortBy(Transformation):
    """Trie les données en fonction de la valeur d'un champ."""
    def __init__(self, field, reverse=False):
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
    """Limite le nombre de lignes affichées."""
    def __init__(self, limit):
        options = {
            'limit': limit
        }
        super().__init__('limit', options)

class ExtractFields(Transformation):
    """Extrait des parties d'un champ en utilisant une expression régulière."""
    def __init__(self, source, regex, rename=None):
        options = {
            'source': source,
            'regex': regex
        }
        if rename:
            options['rename'] = rename
        super().__init__('extractFields', options)

class Debug(Transformation):
    """Affiche le résultat des données à chaque étape."""
    def __init__(self):
        super().__init__('debug')

# --- Dictionnaire pour mapper les noms de transformation YAML aux classes Python ---
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
