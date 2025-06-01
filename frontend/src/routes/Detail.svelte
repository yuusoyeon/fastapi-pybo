<script>
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"
    import { link, push } from 'svelte-spa-router'
    import { is_login, username } from "../lib/store"
    import { marked } from 'marked'
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    export let params = {}
    let question_id = params.question_id
    let question = {answers:[], voter:[], content: ''}
    let content = ""
    let error = {detail:[]}

    // 💬 댓글 관련
    let comment_list = []
    let comment_content = ""

    function get_question() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }

    function get_comments() {
        fastapi("get", "/api/comment/question/" + question_id, {}, (json) => {
            comment_list = json
        })
    }

    function post_comment() {
        if (!comment_content.trim()) return;
        let params = {
            content: comment_content,
            question_id: question_id
        }
        fastapi("post", "/api/comment/create", params,
            (json) => {
                comment_content = ""
                get_comments()
            }
        )
    }

    get_question()
    get_comments()

    function post_answer(event) {
        event.preventDefault()
        let url = "/api/answer/create/" + question_id
        let params = { content }
        fastapi("post", url, params, 
            (json) => {
                content = ""
                error = {detail:[]}
                get_question()
            },
            (err_json) => {
                error = err_json
            }
        )
    }

    function delete_question(_question_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = { question_id: _question_id }
            fastapi('delete', url, params, 
                () => push('/'),
                (err_json) => error = err_json
            )
        }
    }

    function delete_answer(answer_id) {
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = { answer_id }
            fastapi('delete', url, params, 
                () => get_question(),
                (err_json) => error = err_json
            )
        }
    }

    function vote_question(_question_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/question/vote"
            let params = { question_id: _question_id }
            fastapi('post', url, params, 
                () => get_question(),
                (err_json) => error = err_json
            )
        }
    }

    function vote_answer(answer_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/answer/vote"
            let params = { answer_id }
            fastapi('post', url, params, 
                () => get_question(),
                (err_json) => error = err_json
            )
        }
    }
</script>

<div class="container my-3">
    <!-- 질문 -->
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" >
                {@html marked.parse(question.content)}</div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => vote_question(question.id)}> 
                    추천
                    <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
                </button>
                {#if question.user && $username === question.user.username }
                <a use:link href="/question-modify/{question.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_question(question.id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>

    <!-- 💬 댓글 입력/조회 -->
    <div class="card my-3">
        <div class="card-body">
            <h5>💬 댓글</h5>
            <ul>
                {#each comment_list as c}
                    <li>{c.content} <small class="text-muted">({moment(c.create_date).format("MM/DD HH:mm")})</small></li>
                {/each}
            </ul>
            <div class="input-group mt-2">
                <input type="text" class="form-control" bind:value={comment_content} placeholder="댓글을 입력하세요" />
                <button class="btn btn-outline-primary" on:click={post_comment} disabled={!$is_login}>작성</button>
            </div>
        </div>
    </div>

    <button class="btn btn-secondary" on:click={() => push('/')}>목록으로</button>

    <!-- 답변 목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
    {#each question.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" >
                {@html marked.parse(answer.content)}</div>
            <div class="d-flex justify-content-end">
                {#if answer.modify_date }
                <div class="badge bg-light text-dark p-2 text-start mx-3">
                    <div class="mb-2">modified at</div>
                    <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => vote_answer(answer.id)}> 
                    추천
                    <span class="badge rounded-pill bg-success">{ answer.voter.length }</span>
                </button>
                {#if answer.user && $username === answer.user.username }
                <a use:link href="/answer-modify/{answer.id}" 
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                    on:click={() => delete_answer(answer.id)}>삭제</button>
                {/if}
            </div>
        </div>
    </div>
    {/each}

    <!-- 답변 등록 -->
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content}
                disabled={!$is_login} class="form-control"></textarea>
        </div>
        <input type="submit" value="답변등록"
            class="btn btn-primary {$is_login ? '' : 'disabled'}"
            on:click={post_answer} />
    </form>
</div>
