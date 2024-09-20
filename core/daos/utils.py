from typing import Union, Literal


def to_where(join: Union[Literal["AND"], Literal["OR"]] = "AND", **kwargs):
    ret = ""
    if not all(v is None for v in kwargs.values()):
        # need a where clause
        ret += " WHERE"
        for k, v in kwargs.items():
            if v is not None:
                ret += f" {k} = %s {join} "
        ret = ret.removesuffix(f" {join} ")
    return ret
