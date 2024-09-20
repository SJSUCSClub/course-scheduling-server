from typing import Union, Literal


def to_where(join: Union[Literal["AND"], Literal["OR"]] = "AND", **kwargs):
    ret = ""
    if not all(v is None for v in kwargs.values()):
        # need a where clause
        ret += " WHERE"
        for k, v in kwargs.items():
            if v is not None:
                if isinstance(v, list):  # is an array, which means it must be for tags
                    ret += f" {k} @> %s::tag_enum[] {join} "
                else:
                    ret += f" {k} = %s {join} "
        ret = ret.removesuffix(f" {join} ")
    return ret
