import codecs
import pickle
import tipi_tasks

from ..repositories.tags import Tags

class Tagger:

    @staticmethod
    def tag(text):
      tags = Tags.get_all()
      tags = codecs.encode(pickle.dumps(tags), "base64").decode()
      return tipi_tasks.tagger.extract_tags_from_text(text, tags)
