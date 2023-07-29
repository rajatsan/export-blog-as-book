import {  blogger_v3, google } from 'googleapis';
import { writeFileSync } from 'fs';
import { GaxiosResponse } from 'gaxios';

const BLOG_ID = "7345918888953765241";
const API_KEY = ''; // TODO add google API key
const MAX_PAGES = 10;
const PAGE_SIZE = 50;
const TOTAL_POSTS = 428;
const FOLDER_PREFIX = "postsV2";

const blogger = google.blogger({
  version: 'v3',
  auth: API_KEY
});

async function getBlogDetails() {
  const res = await blogger.blogs.get({blogId: BLOG_ID});
  console.log(`The blog url is ${res.data.url}`);
  console.log(res);
}

const getListPostsRequest = (pageToken: undefined | string) => {
  return {
    blogId: BLOG_ID,
    fetchBodies: true, 
    fetchImages: false,
    maxResults: PAGE_SIZE,
    pageToken
  }
}

const getListCommentsRequest = (postId: string) => {
  return {
    blogId: BLOG_ID, 
    postId
  }
};

interface PostWithComments extends blogger_v3.Schema$Post {
  comments?: blogger_v3.Schema$Comment[]
}

const writePostToFile = (post: blogger_v3.Schema$Post) => {
  const fileName = getFileName(post.published || "");
  writeFileSync(fileName, JSON.stringify(post, null, 4));
}

const writePostsToFile = (posts: blogger_v3.Schema$Post[]) => {
  posts.forEach(post => writePostToFile(post));
}

const getFileName = (published: string) => {
  const publishedMillis = Date.parse(published);
  const publishedIso = new Date(publishedMillis).toISOString();
  const publishedIsoCleaned = publishedIso.replace(/[:+-]/g, '_');
  return `${FOLDER_PREFIX}/${publishedIsoCleaned}.json`;
}

async function getPostComments(postId: string) {
  return (await blogger.comments.list(getListCommentsRequest(postId))).data.items
}

async function getPostsWithComments(posts: blogger_v3.Schema$Post[]) {
  // NOTE: only gets the first 20 comments or so. Need to paginate if needed to fetch all
  const postsWithComments: PostWithComments[] = [];
  let totalCommentsCount = 0;
  for (const post of posts) {
    const comments = await getPostComments(post.id as string);
    totalCommentsCount = totalCommentsCount + (comments?.length || 0);
    console.log("Found a total of comments: " + totalCommentsCount);
    postsWithComments.push({
      ...post, 
      comments
    });
  }
  return {
    postsWithComments, totalCommentsCount
  };
}

async function getPosts() {
  let pageToken: undefined | string;
  let allPosts: blogger_v3.Schema$Post[] = [];
  let allCommentsCount = 0;

  for (let currPage = 0; currPage < MAX_PAGES; currPage++) {
    const currPagePostsResult: GaxiosResponse<blogger_v3.Schema$PostList> = await blogger.posts.list(getListPostsRequest(pageToken));
    const nextPageToken = currPagePostsResult.data.nextPageToken;
    const currPagePosts = currPagePostsResult.data.items || [];

    const currPagePostsWithComments = await getPostsWithComments(currPagePosts);

    writePostsToFile(currPagePostsWithComments.postsWithComments);
    allCommentsCount = allCommentsCount + currPagePostsWithComments.totalCommentsCount;

    allPosts = [...allPosts, ...currPagePosts];

    if (!nextPageToken) {
      console.log("Reached end of results. Exiting...")
      break;
    }

    pageToken = nextPageToken;
    console.log("pageToken: " + pageToken);
  }

  console.log(`Found a total of ${allPosts.length} posts`);
  console.log(`Wrote a total of ${allCommentsCount} comments`);
}



getPosts().catch(console.error);
