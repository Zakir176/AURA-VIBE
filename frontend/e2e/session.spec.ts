import { test, expect } from '@playwright/test';

test.describe('Session Flow', () => {
  test('should allow a user to create a session, add a song, and see it in the queue', async ({ page }) => {
    // Mock API responses
    await page.route('**/api/session/create', async route => {
      await route.fulfill({
        json: {
          session_code: 'TEST1234',
          qr_code: 'qr_code_base64',
          host_id: 'test_host_id',
          name: 'Test Session',
          duration: '1hr'
        }
      });
    });

    await page.route('**/api/search?query=test&provider=jamendo', async route => {
      await route.fulfill({
        json: {
          provider: 'jamendo',
          tracks: [{ id: '123', name: 'Test Song', artist_name: 'Test Artist', audio: 'url', image: 'img' }]
        }
      });
    });

    await page.route('**/api/queue/add', async route => {
        await route.fulfill({
            json: {
                id: 1,
                song_id: "123",
                song_title: "Test Song",
                artist_name: "Test Artist",
                song_url: "url",
                image: "img",
                added_by: "user1",
                votes: 0,
                user_vote_type: null
            }
        });
    });

    let queueListRequestCount = 0;
    await page.route('**/api/queue/list/TEST1234**', async route => {
        queueListRequestCount++;
        if (queueListRequestCount <= 1) {
            // First call on page load is an empty queue
            await route.fulfill({ json: [] });
        } else {
            // Subsequent calls (after adding a song) return the updated queue
            await route.fulfill({
                json: [{ id: 1, song_id: '123', name: 'Test Song', artist_name: 'Test Artist', audio: 'url', image: 'img', added_by: 'user1', votes: 0, user_vote_type: null }]
            });
        }
    });

    // Start on the landing page
    await page.goto('/');

    // Click on create session button
    await page.getByRole('link', { name: 'Create Session' }).click();

    // Fill in session name
    await page.getByLabel('Name Your Vibe').fill('Test Session');
    
    // Click create and start session
    await page.getByRole('button', { name: 'Create & Start Session' }).click();
    
    // Wait for navigation to session page
    await page.waitForURL('**/session/TEST1234');
    await expect(page.getByText('ROOM #TEST1234')).toBeVisible();

    // Search for a song
    const searchBar = page.getByPlaceholder('Search for a song...');
    await searchBar.fill('test');

    // Click on the search result
    await page.getByText('Test Song').click();

    // Expect the song to be in the queue
    await expect(page.getByText('Up Next')).toBeVisible();
    const queueList = page.locator('.space-y-3');
    await expect(queueList.getByText('Test Song')).toBeVisible();
  });
});
