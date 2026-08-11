import pytest

from app.core.document_qa_service import DocumentQAService


def test_empty_question_is_rejected():

    service = DocumentQAService()

    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        service.ask("")


def test_whitespace_question_is_rejected():

    service = DocumentQAService()

    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        service.ask("   ")


def test_none_question_is_rejected():

    service = DocumentQAService()

    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        service.ask(None)


def test_invalid_document_path_is_rejected():

    service = DocumentQAService()

    with pytest.raises(
        FileNotFoundError,
        match="Document not found",
    ):
        service.index_document(
            "documents/does_not_exist.pdf"
        )