import pytest
from retrieval import chunks
def test_overlap():
 result=list(chunks("0 1 2 3 4 5 6 7",4,1));assert result==["0 1 2 3","3 4 5 6","6 7"]
def test_invalid():
 with pytest.raises(ValueError):list(chunks("text",5,5))
